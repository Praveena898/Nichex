"""
Extracts MFCC (Mel-Frequency Cepstral Coefficient) features from audio
files and saves them as numpy arrays — the input format your CNN needs.

What MFCCs actually capture:
- They model how the human ear perceives sound (mel scale) and compress
  the frequency spectrum into ~40 coefficients per time frame.
- Real human voices have natural irregularities in these coefficients
  (breathing, vocal tract resonance quirks). AI-generated voices often
  have subtly TOO-smooth or repetitive patterns here — that's the signal
  your CNN will learn to detect.

Output shape per file: (n_mfcc, time_steps) — e.g. (40, 130) for a
3-second clip. This is treated like a grayscale image by the CNN.
"""

import librosa
import numpy as np
import os

SR = 16000          # sample rate — ASVspoof audio is 16kHz, resample if needed
N_MFCC = 40          # number of MFCC coefficients (40 is standard for speech)
DURATION = 3.0       # seconds — pad/trim every clip to the same length
MAX_FRAMES = 130     # matches ~3 sec at default hop_length=512, sr=16000


def extract_mfcc(filepath, sr=SR, n_mfcc=N_MFCC, duration=DURATION, max_frames=MAX_FRAMES):
    """
    Loads one audio file and returns a fixed-size MFCC feature array.
    """
    # Load audio, resample to 16kHz, force mono
    y, _ = librosa.load(filepath, sr=sr, mono=True, duration=duration)

    # Pad with silence if the clip is shorter than `duration`
    target_len = int(sr * duration)
    if len(y) < target_len:
        y = np.pad(y, (0, target_len - len(y)))

    # Extract MFCCs: shape becomes (n_mfcc, time_steps)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    # Force every file to the exact same time_steps length
    # (needed because the CNN expects a fixed input shape)
    if mfcc.shape[1] < max_frames:
        pad_width = max_frames - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode="constant")
    else:
        mfcc = mfcc[:, :max_frames]

    # Normalize (zero mean, unit variance) — helps the CNN train faster
    mfcc = (mfcc - mfcc.mean()) / (mfcc.std() + 1e-8)

    return mfcc  # shape: (40, 130)


def process_dataset(file_label_csv, output_dir, sr=SR, n_mfcc=N_MFCC):
    """
    Reads a CSV with columns ['filepath', 'label'], extracts MFCCs for
    every file, and saves each as a .npy file plus one combined array.
    """
    import pandas as pd
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

    features = np.array(features)  # shape: (num_files, 40, 130)
    labels = np.array(labels)

    np.save(os.path.join(output_dir, "mfcc_features.npy"), features)
    np.save(os.path.join(output_dir, "labels.npy"), labels)
    print(f"\nSaved {features.shape[0]} samples, feature shape {features.shape[1:]}")
    print(f"Files: {output_dir}/mfcc_features.npy and labels.npy")

    return features, labels


if __name__ == "__main__":
    # Quick demo: generate a synthetic sine wave as a stand-in for a real
    # audio file, just to prove the pipeline works end-to-end.
    import soundfile as sf

    demo_audio_path = "/home/claude/digital_bodyguard/data/demo_audio.wav"
    t = np.linspace(0, 3, int(SR * 3))
    demo_wave = 0.3 * np.sin(2 * np.pi * 220 * t)  # 220Hz tone, 3 seconds
    sf.write(demo_audio_path, demo_wave, SR)

    mfcc_features = extract_mfcc(demo_audio_path)
    print(f"MFCC shape: {mfcc_features.shape}")  # should be (40, 130)
    print(f"Sample values (first 5 of first row): {mfcc_features[0][:5]}")

    print("\n--- To process your real ASVspoof dataset ---")
    print("1. Create a CSV with columns: filepath, label (0=real, 1=fake)")
    print("2. Run: process_dataset('data/asvspoof_filelist.csv', 'data/mfcc_output')")
