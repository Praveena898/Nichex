"""
Quick fine-tune so real-world noisy recordings (your own voice clips)
are treated as bonafide (label 0).

Use this when the CNN was trained on clean ASVspoof studio audio and
flags phone/mic recordings as fake. For best results, also run full
MUSAN augmentation + retrain when you have ASVspoof + MUSAN audio.

Usage:
  python scripts/finetune_bonafide_clips.py \\
      --audio "C:/Users/sarah/Downloads/Green sarah voice.m4a" \\
      --musan "C:/Users/sarah/Downloads/musan/musan" \\
      --copies 40
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
    noise_files = collect_musan_noise_files(musan_root) if musan_root else []
    features = []

    for path in audio_paths:
        clean = load_audio_mono(path, sr=SR, duration=None)
        clean = preprocess_speech_waveform(clean, sr=SR, clip_duration=3.0)
        features.append(extract_mfcc(clean, sr=SR, is_array=True, already_preprocessed=True))

        for _ in range(copies_per_file):
            if noise_files:
                noise = load_audio_mono(random.choice(noise_files), sr=SR, duration=3.0)
            else:
                noise = synthetic_noise(len(clean))
            snr = random.uniform(*snr_range)
            noisy = mix_at_snr(clean, noise, snr_db=snr)
            features.append(
                extract_mfcc(noisy, sr=SR, is_array=True, already_preprocessed=True)
            )

    x = torch.tensor(np.array(features), dtype=torch.float32).unsqueeze(1)
    y = torch.zeros((len(features), 1), dtype=torch.float32)
    return x, y


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--audio-folder",
        required=True,
        help="Folder containing real recordings"
    )
    parser.add_argument("--musan", default="", help="MUSAN root (optional)")
    parser.add_argument("--copies", type=int, default=30)
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--snr-min", type=float, default=3.0)
    parser.add_argument("--snr-max", type=float, default=18.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    audio_paths = []

    for ext in ("*.wav", "*.mp3", "*.m4a", "*.flac"):
        audio_paths.extend(Path(args.audio_folder).glob(ext))

    audio_paths = [str(p) for p in audio_paths]

    print(f"Found {len(audio_paths)} recordings.")

    random.seed(args.seed)
    np.random.seed(args.seed)

    x, y = build_bonafide_features(
        audio_paths,
        args.musan or None,
        args.copies,
        (args.snr_min, args.snr_max),
    )
    loader = DataLoader(TensorDataset(x, y), batch_size=min(16, len(x)), shuffle=True)

    model = DeepfakeCNN().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))

    for param in model.conv.parameters():
        param.requires_grad = False

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.fc.parameters(), lr=args.lr)

    for epoch in range(1, args.epochs + 1):
        model.train()
        epoch_loss = 0.0
        for x_batch, y_batch in loader:
            x_batch, y_batch = x_batch.to(DEVICE), y_batch.to(DEVICE)
            optimizer.zero_grad()
            out = model(x_batch)
            loss = criterion(out, y_batch)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * x_batch.size(0)
        print(f"Epoch {epoch}/{args.epochs} loss={epoch_loss / len(x):.4f}")

    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Updated {MODEL_PATH} with {len(x)} bonafide (noisy) samples.")


if __name__ == "__main__":
    main()
