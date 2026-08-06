"""
Extracts MFCC (Mel-Frequency Cepstral Coefficient) features from audio
files and saves them as numpy arrays — the input format your CNN needs.
"""

import os

import numpy as np
import pandas as pd

import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.features.mfcc_extractor import extract_mfcc, N_MFCC
from src.features.audio_preprocess import SR


def process_dataset(file_label_csv, output_dir, sr=SR, n_mfcc=N_MFCC):
    """
    Reads a CSV with columns ['filepath', 'label'], extracts MFCCs for
    every file, and saves each as a .npy file plus one combined array.
    """
    df = pd.read_csv(file_label_csv)
    os.makedirs(output_dir, exist_ok=True)

    features, labels = [], []
    for i, row in df.iterrows():
        try:
            mfcc = extract_mfcc(row["filepath"], sr=sr, n_mfcc=n_mfcc)
            features.append(mfcc)
            labels.append(row["label"])
        except Exception as e:
            print(f"Skipped {row['filepath']}: {e}")

        if i % 50 == 0:
            print(f"Processed {i}/{len(df)}")

    features = np.array(features)
    labels = np.array(labels)

    np.save(os.path.join(output_dir, "mfcc_features.npy"), features)
    np.save(os.path.join(output_dir, "labels.npy"), labels)
    print(f"\nSaved {features.shape[0]} samples, feature shape {features.shape[1:]}")
    print(f"Files: {output_dir}/mfcc_features.npy and labels.npy")

    return features, labels


if __name__ == "__main__":
    print("--- To process your ASVspoof dataset ---")
    print("1. Create a CSV with columns: filepath, label (0=real, 1=fake)")
    print("2. Run: process_dataset('data/asvspoof_filelist.csv', 'data/mfcc_output')")
