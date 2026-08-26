"""
Fine-tune so real-world noisy recordings (your own voice clips) are
treated as bonafide (label 0), WITHOUT catastrophically forgetting
ASVspoof spoof detection.

Key difference from the earlier version: fine-tuning batches now mix
real-world bonafide samples with a REPLAY sample of ASVspoof bonafide
+ spoof features (loaded from your existing extracted
data/mfcc_output/mfcc_features.npy + labels.npy). This prevents the FC
layers from collapsing onto a trivial "always predict real" solution,
which is what happened when fine-tuning saw only label-0 examples.

Usage:
  python scripts/finetune_bonafide_clips.py \\
      --audio-folder "C:/Users/sarah/Downloads/real_world_clips" \\
      --musan "C:/Users/sarah/Downloads/musan/musan" \\
      --copies 40 \\
      --replay-per-class 1500
"""

from __future__ import annotations

import argparse
import os
import random
import sys

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from pathlib import Path
from sklearn.model_selection import train_test_split

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.features.audio_preprocess import (
    SR,
    collect_musan_noise_files,
    load_audio_mono,
    mix_at_snr,
    preprocess_speech_waveform,
)
from src.features.mfcc_extractor import extract_mfcc
from src.models.deepfake_cnn import DeepfakeCNN

MODEL_PATH = "models/deepfake_cnn.pth"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def synthetic_noise(n: int) -> np.ndarray:
    return (np.random.randn(n).astype(np.float32) * 0.02)


def build_bonafide_features(audio_paths, musan_root, copies_per_file, snr_range):
    """
    Noise is mixed into RAW audio, then the FULL preprocess_speech_waveform
    pipeline (bandpass -> noisereduce -> RMS normalize -> window) is applied
    AFTER mixing, on every sample -- matching exactly what happens to a real
    noisy recording at inference time.
    """
    noise_files = collect_musan_noise_files(musan_root) if musan_root else []
    features = []

    for path in audio_paths:
        raw = load_audio_mono(path, sr=SR, duration=None)

        clean_processed = preprocess_speech_waveform(raw, sr=SR, clip_duration=3.0)
        features.append(
            extract_mfcc(clean_processed, sr=SR, is_array=True, already_preprocessed=True)
        )

        for _ in range(copies_per_file):
            if noise_files:
                noise = load_audio_mono(random.choice(noise_files), sr=SR, duration=3.0)
            else:
                noise = synthetic_noise(len(raw))
            snr = random.uniform(*snr_range)

            noisy_raw = mix_at_snr(raw, noise, snr_db=snr)
            noisy_processed = preprocess_speech_waveform(noisy_raw, sr=SR, clip_duration=3.0)

            features.append(
                extract_mfcc(noisy_processed, sr=SR, is_array=True, already_preprocessed=True)
            )

    x = np.array(features, dtype=np.float32)
    y = np.zeros((len(features), 1), dtype=np.float32)
    return x, y


def load_replay_samples(mfcc_path, labels_path, per_class, seed):
    """
    Samples `per_class` bonafide AND `per_class` spoof examples from the
    already-extracted ASVspoof training features, so fine-tuning batches
    keep seeing both classes and can't collapse toward "always real".
    """
    if not os.path.exists(mfcc_path) or not os.path.exists(labels_path):
        raise FileNotFoundError(
            f"Replay data not found at {mfcc_path} / {labels_path}. "
            "These are the same files produced by scripts/extract_mfcc.py "
            "during original ASVspoof training -- run that first if missing."
        )

    features = np.load(mfcc_path)
    labels = np.load(labels_path)

    rng = np.random.default_rng(seed)
    replay_x, replay_y = [], []

    for class_label in (0, 1):
        idx = np.where(labels == class_label)[0]
        if len(idx) == 0:
            print(f"WARNING: no class-{class_label} samples found in replay data.")
            continue
        n = min(per_class, len(idx))
        chosen = rng.choice(idx, size=n, replace=False)
        replay_x.append(features[chosen])
        replay_y.append(labels[chosen].reshape(-1, 1).astype(np.float32))

    replay_x = np.concatenate(replay_x, axis=0)
    replay_y = np.concatenate(replay_y, axis=0)
    print(f"Loaded replay set: {replay_x.shape[0]} samples "
          f"({int((replay_y == 0).sum())} bonafide, {int((replay_y == 1).sum())} spoof)")
    return replay_x, replay_y


def evaluate(model, loader, criterion):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    tp = fp = tn = fn = 0
    with torch.no_grad():
        for x_batch, y_batch in loader:
            x_batch, y_batch = x_batch.to(DEVICE), y_batch.to(DEVICE)
            out = model(x_batch)
            loss = criterion(out, y_batch)
            total_loss += loss.item() * x_batch.size(0)
            pred = (out > 0.5).float()
            correct += (pred == y_batch).sum().item()
            total += y_batch.size(0)
            tp += ((pred == 1) & (y_batch == 1)).sum().item()
            fp += ((pred == 1) & (y_batch == 0)).sum().item()
            tn += ((pred == 0) & (y_batch == 0)).sum().item()
            fn += ((pred == 0) & (y_batch == 1)).sum().item()

    acc = correct / total
    fake_recall = tp / (tp + fn) if (tp + fn) > 0 else float("nan")
    real_recall = tn / (tn + fp) if (tn + fp) > 0 else float("nan")
    return total_loss / total, acc, fake_recall, real_recall


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-folder", required=True, help="Folder containing real recordings")
    parser.add_argument("--musan", default="", help="MUSAN root (optional)")
    parser.add_argument("--copies", type=int, default=40)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--snr-min", type=float, default=3.0)
    parser.add_argument("--snr-max", type=float, default=18.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--replay-mfcc", default="data/mfcc_output/mfcc_features.npy")
    parser.add_argument("--replay-labels", default="data/mfcc_output/labels.npy")
    parser.add_argument("--replay-per-class", type=int, default=1500)
    parser.add_argument("--val-fraction", type=float, default=0.15)
    parser.add_argument("--patience", type=int, default=3, help="Early-stopping patience (epochs)")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    audio_paths = []
    for ext in ("*.wav", "*.mp3", "*.m4a", "*.flac"):
        audio_paths.extend(Path(args.audio_folder).glob(ext))
    audio_paths = [str(p) for p in audio_paths]
    print(f"Found {len(audio_paths)} real-world recordings.")

    real_x, real_y = build_bonafide_features(
        audio_paths, args.musan or None, args.copies, (args.snr_min, args.snr_max)
    )
    replay_x, replay_y = load_replay_samples(
        args.replay_mfcc, args.replay_labels, args.replay_per_class, args.seed
    )

    all_x = np.concatenate([real_x, replay_x], axis=0)
    all_y = np.concatenate([real_y, replay_y], axis=0)
    print(f"Combined fine-tuning set: {all_x.shape[0]} samples "
          f"({int((all_y == 0).sum())} bonafide / {int((all_y == 1).sum())} spoof)")

    x_train, x_val, y_train, y_val = train_test_split(
        all_x, all_y, test_size=args.val_fraction, random_state=args.seed, stratify=all_y
    )

    def to_loader(x, y, shuffle):
        x_t = torch.tensor(x, dtype=torch.float32).unsqueeze(1)
        y_t = torch.tensor(y, dtype=torch.float32)
        return DataLoader(TensorDataset(x_t, y_t), batch_size=32, shuffle=shuffle)

    train_loader = to_loader(x_train, y_train, shuffle=True)
    val_loader = to_loader(x_val, y_val, shuffle=False)

    model = DeepfakeCNN().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))

    for param in model.conv.parameters():
        param.requires_grad = False

    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.fc.parameters(), lr=args.lr)

    best_val_loss = float("inf")
    epochs_without_improvement = 0
    best_path = "models/deepfake_cnn_finetuned_candidate.pth"
    os.makedirs("models", exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        model.train()
        train_loss = 0.0
        for x_batch, y_batch in train_loader:
            x_batch, y_batch = x_batch.to(DEVICE), y_batch.to(DEVICE)
            optimizer.zero_grad()
            out = model(x_batch)
            loss = criterion(out, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * x_batch.size(0)
        train_loss /= len(train_loader.dataset)

        val_loss, val_acc, val_fake_recall, val_real_recall = evaluate(model, val_loader, criterion)
        print(f"Epoch {epoch}/{args.epochs} | train_loss={train_loss:.4f} | "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.4f} "
              f"val_fake_recall={val_fake_recall:.4f} val_real_recall={val_real_recall:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_without_improvement = 0
            torch.save(model.state_dict(), best_path)
            print(f"  -> New best checkpoint saved (val_loss={val_loss:.4f})")
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= args.patience:
                print(f"Early stopping: no improvement for {args.patience} epochs.")
                break

    print(f"\nBest candidate model saved to: {best_path}")
    print("This candidate has NOT replaced models/deepfake_cnn.pth.")
    print("Run scripts/evaluate_deepfake_cnn.py and your real-world held-out test")
    print("against this candidate BEFORE deciding whether to promote it. See the")
    print("promotion command in the assistant's reply.")


if __name__ == "__main__":
    main()