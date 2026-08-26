"""
Whisper transcription tuned for noisy phone-style recordings.
"""

from __future__ import annotations

import os

import numpy as np

from src.features.audio_preprocess import SR, preprocess_speech_waveform, load_audio_mono

WHISPER_MODEL_NAME = os.environ.get("WHISPER_MODEL", "large")
WHISPER_LANGUAGE = os.environ.get("WHISPER_LANGUAGE", None)


def transcribe_with_whisper(whisper_model, audio_path: str) -> tuple[str, float,str]:
    """
    Returns (transcript, confidence in 0–1).
    Confidence is low when Whisper is guessing/hallucinating on noise.
    """
    y = load_audio_mono(audio_path, sr=SR, duration=None)
    y = preprocess_speech_waveform(
        y, sr=SR, clip_duration=None, pick_loudest_window=False
    )

    kwargs = dict(
        fp16=False,
        condition_on_previous_text=False,
        no_speech_threshold=0.6,
        logprob_threshold=-1.0,
        compression_ratio_threshold=2.4,
        initial_prompt=(
            "Phone call conversation. "
            "The speakers may speak English, Hindi, Tamil, or Malayalam."
        )
    )

    if WHISPER_LANGUAGE:
        kwargs["language"] = WHISPER_LANGUAGE

    result = whisper_model.transcribe(y, **kwargs)

    text = (result.get("text") or "").strip()
    confidence = _transcript_confidence(result)
    language = (result.get("language") or "en").lower()


    return text, confidence, language

def _transcript_confidence(result: dict) -> float:
    segments = result.get("segments") or []
    if not segments:
        text = (result.get("text") or "").strip()
        return 0.0 if not text else 0.35

    no_speech = [float(s.get("no_speech_prob", 0.5)) for s in segments]
    logprobs = [float(s.get("avg_logprob", -1.0)) for s in segments if "avg_logprob" in s]

    speech_score = 1.0 - float(np.mean(no_speech))
    if logprobs:
        # Typical good English logprobs are around -0.3 to -0.8
        logprob_score = float(np.clip((np.mean(logprobs) + 1.2) / 1.0, 0.0, 1.0))
    else:
        logprob_score = 0.4

    return float(np.clip(0.55 * speech_score + 0.45 * logprob_score, 0.0, 1.0))
