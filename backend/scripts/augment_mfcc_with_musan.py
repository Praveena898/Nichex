"""
Expand MFCC training data by mixing MUSAN noise/music into ASVspoof clips.

Teaches the deepfake CNN that background noise alone does not mean "fake".

Prerequisites:
  1. Full MUSAN corpus (not just README/LICENSE) under e.g. Downloads/musan/musan
  2. A CSV with columns: filepath, label  (0=bonafide/real, 1=spoof/fake)
  3. pip install -r requirements.txt

Usage (from backend/):
  python scripts/augment_mfcc_with_musan.py \\
      --csv data/asvspoof_filelist.csv \\
      --musan "C:/Users/sarah/Downloads/musan/musan" \\
      --output-dir data/mfcc_output_noisy \\
      --copies-per-file 2

Then train on the augmented arrays:
  python scripts/train_deepfake_cnn.py
  (set MFCC_PATH / LABELS_PATH to data/mfcc_output_noisy/…)
"""

from __future__ import annotations

import argparse
import os
import random
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.features.audio_preprocess import (
    SR,
    collect_musan_noise_files,
    load_audio_mono,
    mix_at_snr,
    preprocess_speech_waveform,
)
from src.features.mfcc_extractor import extract_mfcc


def _random_noise(clean: np.ndarray) -> np.ndarray:
    return np.random.randn(len(clean)).astype(np.float32) * 0.02


def main():
    parser = argparse.ArgumentParser(description="Augment MFCC dataset with MUSAN noise")
    parser.add_argument("--csv", required=True, help="filepath,label CSV")
    parser.add_argument("--musan", required=True, help="Path to musan root (contains noise/, music/)")
    parser.add_argument("--output-dir", default="data/mfcc_output_noisy")
    parser.add_argument("--copies-per-file", type=int, default=2)
    parser.add_argument("--snr-min", type=float, default=5.0)
    parser.add_argument("--snr-max", type=float, default=20.0)
    parser.add_argument(
        "--allow-synthetic-noise",
        action="store_true",
        help="If MUSAN has no audio files, mix with synthetic noise instead of failing",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    noise_files = collect_musan_noise_files(args.musan)
    use_synthetic = False
    if not noise_files:
        if args.allow_synthetic_noise:
            use_synthetic = True
            print("MUSAN audio not found — using synthetic noise for augmentation.")
        else:
            raise SystemExit(
                f"No .wav/.flac files under {args.musan}/noise or .../music.\n"
                "Download full MUSAN from https://www.openslr.org/17/ "
                "or pass --allow-synthetic-noise."
            )

    df = pd.read_csv(args.csv)
    os.makedirs(args.output_dir, exist_ok=True)

    features = []
    labels = []

    for i, row in df.iterrows():
        path = row["filepath"]
        label = int(row["label"])
        try:
            mfcc_clean = extract_mfcc(path, sr=SR)
            features.append(mfcc_clean)
            labels.append(label)

            clean = load_audio_mono(path, sr=SR, duration=None)
            clean = preprocess_speech_waveform(clean, sr=SR, clip_duration=3.0)

            for _ in range(args.copies_per_file):
                snr = random.uniform(args.snr_min, args.snr_max)
                if use_synthetic:
                    noise = _random_noise(clean)
                else:
                    noise_path = random.choice(noise_files)
                    noise = load_audio_mono(noise_path, sr=SR, duration=3.0)
                noisy = mix_at_snr(clean, noise, snr_db=snr)
                mfcc_noisy = extract_mfcc(
                    noisy, sr=SR, is_array=True, already_preprocessed=True
                )
                features.append(mfcc_noisy)
                labels.append(label)
        except Exception as exc:
            print(f"Skipped {path}: {exc}")

        if i and i % 50 == 0:
            print(f"Processed {i}/{len(df)}")

    features_arr = np.array(features)
    labels_arr = np.array(labels)
    np.save(os.path.join(args.output_dir, "mfcc_features.npy"), features_arr)
    np.save(os.path.join(args.output_dir, "labels.npy"), labels_arr)
    print(
        f"Saved {features_arr.shape[0]} samples to {args.output_dir} "
        f"(shape {features_arr.shape[1:]})"
    )


if __name__ == "__main__":
    main()
