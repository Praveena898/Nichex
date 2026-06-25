"""
Reusable MFCC extraction — imported by both training code and the
live demo pipeline (unlike scripts/extract_mfcc.py, which is a one-time
batch-processing script you run from the command line).

Usage:
    from src.features.mfcc_extractor import extract_mfcc
    features = extract_mfcc("path/to/call_chunk.wav")
"""

import librosa
import numpy as np

SR = 16000
N_MFCC = 40
DURATION = 3.0
MAX_FRAMES = 130


def extract_mfcc(filepath_or_array, sr=SR, n_mfcc=N_MFCC, duration=DURATION, max_frames=MAX_FRAMES, is_array=False):
    """
    Extracts a fixed-size, normalized MFCC array from either:
    - a filepath to a .wav file, OR
    - a raw numpy audio array already in memory (e.g. live mic chunk)

    Returns shape (n_mfcc, max_frames), e.g. (40, 130)
    """
    if is_array:
        y = filepath_or_array
    else:
        y, _ = librosa.load(filepath_or_array, sr=sr, mono=True, duration=duration)

    target_len = int(sr * duration)
    if len(y) < target_len:
        y = np.pad(y, (0, target_len - len(y)))
    else:
        y = y[:target_len]

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    if mfcc.shape[1] < max_frames:
        mfcc = np.pad(mfcc, ((0, 0), (0, max_frames - mfcc.shape[1])), mode="constant")
    else:
        mfcc = mfcc[:, :max_frames]

    mfcc = (mfcc - mfcc.mean()) / (mfcc.std() + 1e-8)
    return mfcc
