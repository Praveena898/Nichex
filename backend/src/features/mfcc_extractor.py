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

from src.features.audio_preprocess import (
    SR,
    DURATION,
    load_audio_mono,
    preprocess_speech_waveform,
)

N_MFCC = 40
MAX_FRAMES = 130


def extract_mfcc(
    filepath_or_array,
    sr=SR,
    n_mfcc=N_MFCC,
    duration=DURATION,
    max_frames=MAX_FRAMES,
    is_array=False,
    already_preprocessed=False,
):
    """
    Extracts a fixed-size, normalized MFCC array from either:
    - a filepath to an audio file, OR
    - a raw numpy audio array already in memory (e.g. live mic chunk)

    Returns shape (n_mfcc, max_frames), e.g. (40, 130)
    """

    if is_array:
        if already_preprocessed:
            y = filepath_or_array.astype(np.float32)
            target_len = int(sr * duration)
            if len(y) < target_len:
                y = np.pad(y, (0, target_len - len(y)))
            else:
                y = y[:target_len]
        else:
            y = preprocess_speech_waveform(
                filepath_or_array.astype(np.float32),
                sr=sr,
                clip_duration=duration,
                pick_loudest_window=True,
            )
    else:
        y = load_audio_mono(filepath_or_array, sr=sr, duration=None)
        y = preprocess_speech_waveform(
            y, sr=sr, clip_duration=duration, pick_loudest_window=True
        )

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    if mfcc.shape[1] < max_frames:
        mfcc = np.pad(mfcc, ((0, 0), (0, max_frames - mfcc.shape[1])), mode="constant")
    else:
        mfcc = mfcc[:, :max_frames]

    mfcc = (mfcc - mfcc.mean()) / (mfcc.std() + 1e-8)
    return mfcc
