"""
Speech-focused audio loading and preprocessing shared by MFCC extraction,
Whisper transcription, and MUSAN noise-augmentation training.
"""

from __future__ import annotations

import os
from pathlib import Path

import librosa
import numpy as np

SR = 16000
DURATION = 3.0


def reduce_background_noise(y: np.ndarray, sr: int = SR) -> np.ndarray:
    try:
        import noisereduce as nr

        return nr.reduce_noise(y=y, sr=sr, stationary=True, prop_decrease=0.75)
    except ImportError:
        return y


def bandpass_speech(y: np.ndarray, sr: int = SR) -> np.ndarray:
    """Keep typical telephony/speech band to reduce unrelated background."""
    try:
        from scipy.signal import butter, sosfilt

        sos = butter(4, [80, 7600], btype="bandpass", fs=sr, output="sos")
        return sosfilt(sos, y).astype(np.float32)
    except Exception:
        return y


def normalize_rms(y: np.ndarray, target_rms: float = 0.08) -> np.ndarray:
    rms = float(np.sqrt(np.mean(np.square(y)) + 1e-12))
    if rms < 1e-6:
        return y
    return (y * (target_rms / rms)).astype(np.float32)


def select_loudest_window(y: np.ndarray, sr: int, duration: float = DURATION) -> np.ndarray:
    """
    Pick the `duration`-second slice with the most speech-like energy instead
    of always using the first few seconds (which are often silence or noise).
    """
    target_len = int(sr * duration)
    if len(y) <= target_len:
        return y

    hop = 512
    frame_length = 2048
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop)[0]
    frames_needed = max(1, int(np.ceil(target_len / hop)))

    if len(rms) <= frames_needed:
        return y[:target_len]

    window_sums = np.convolve(rms, np.ones(frames_needed, dtype=np.float32), mode="valid")
    best_frame = int(np.argmax(window_sums))
    start = best_frame * hop
    end = start + target_len
    if end > len(y):
        end = len(y)
        start = max(0, end - target_len)
    return y[start:end]


def load_audio_mono(
    path: str | os.PathLike,
    sr: int = SR,
    duration: float | None = None,
) -> np.ndarray:
    """Load any format librosa/ffmpeg supports (.wav, .flac, .m4a, …)."""
    y, _ = librosa.load(str(path), sr=sr, mono=True, duration=duration)
    return y.astype(np.float32)


def preprocess_speech_waveform(
    y: np.ndarray,
    sr: int = SR,
    clip_duration: float | None = DURATION,
    pick_loudest_window: bool = True,
) -> np.ndarray:
    y = bandpass_speech(y, sr=sr)
    y = reduce_background_noise(y, sr=sr)
    y = normalize_rms(y)

    if clip_duration is not None:
        if pick_loudest_window:
            y = select_loudest_window(y, sr, duration=clip_duration)
        target_len = int(sr * clip_duration)
        if len(y) < target_len:
            y = np.pad(y, (0, target_len - len(y)))
        else:
            y = y[:target_len]

    return y.astype(np.float32)


def preprocess_speech_file(
    path: str | os.PathLike,
    sr: int = SR,
    clip_duration: float | None = DURATION,
    pick_loudest_window: bool = True,
) -> np.ndarray:
    y = load_audio_mono(path, sr=sr, duration=None)
    return preprocess_speech_waveform(
        y,
        sr=sr,
        clip_duration=clip_duration,
        pick_loudest_window=pick_loudest_window,
    )


def mix_at_snr(clean: np.ndarray, noise: np.ndarray, snr_db: float) -> np.ndarray:
    """Mix noise into clean speech at the given signal-to-noise ratio (dB)."""
    clean = clean.astype(np.float32)
    noise = noise.astype(np.float32)

    if len(noise) < len(clean):
        reps = int(np.ceil(len(clean) / len(noise)))
        noise = np.tile(noise, reps)
    noise = noise[: len(clean)]

    clean_power = np.mean(clean ** 2) + 1e-12
    noise_power = np.mean(noise ** 2) + 1e-12
    target_noise_power = clean_power / (10 ** (snr_db / 10))
    noise = noise * np.sqrt(target_noise_power / noise_power)

    mixed = clean + noise
    peak = np.max(np.abs(mixed)) + 1e-12
    if peak > 0.99:
        mixed = mixed * (0.99 / peak)
    return mixed.astype(np.float32)


def collect_musan_noise_files(musan_root: str | os.PathLike) -> list[Path]:
    root = Path(musan_root)
    noise_dirs = [root / "noise", root / "music"]
    files: list[Path] = []
    for directory in noise_dirs:
        if not directory.is_dir():
            continue
        files.extend(directory.rglob("*.wav"))
        files.extend(directory.rglob("*.flac"))
    return sorted(files)
