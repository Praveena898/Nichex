"""
The full Digital Bodyguard pipeline — connects both trained models into
one function you call with an audio file and get back a real risk assessment.

This is the core of Phase 4: replacing the hand-typed test numbers in
risk_engine.py with real outputs from real trained models.

Flow:
    audio file (.flac/.wav)
        ↓
    mfcc_extractor  →  deepfake_cnn  →  deepfake_prob (real)
        ↓
    whisper STT  →  scam_nlp  →  scam_language_prob (real)
        ↓
    risk_engine  →  score + color + alert_family (real)

Usage:
    from src.pipeline import analyze_audio_file
    result = analyze_audio_file("path/to/audio.wav")
    print(result)
"""

import os
import sys
import torch
import whisper

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.features.mfcc_extractor import extract_mfcc
from src.models.deepfake_cnn import load_deepfake_model, predict_deepfake_probability
from src.models.scam_nlp import ScamNLPModel, keyword_score
from src.risk_engine import assess_call_chunk

# Paths to your trained models
DEEPFAKE_MODEL_PATH = r"C:\Users\prave\OneDrive\Desktop\DigitalBodyguard\Nichex\backend\models\deepfake_cnn.pth"
SCAM_MODEL_PATH = r"C:\Users\prave\OneDrive\Desktop\DigitalBodyguard\Nichex\backend\models\scam_distilbert"

# Load once at module level so they're not reloaded on every call
# (loading takes ~2-3 seconds; you don't want that per audio chunk)
_deepfake_model = None
_scam_model = None
_whisper_model = None


def _load_models():
    """Lazy-loads all three models on first call, caches for reuse."""
    global _deepfake_model, _scam_model, _whisper_model

    if _deepfake_model is None:
        print("Loading deepfake CNN model...")
        _deepfake_model = load_deepfake_model(DEEPFAKE_MODEL_PATH)

    if _scam_model is None:
        print("Loading scam NLP model...")
        _scam_model = ScamNLPModel(model_path=SCAM_MODEL_PATH)

    if _whisper_model is None:
        print("Loading Whisper speech-to-text model (tiny)...")
        # 'tiny' is fastest and sufficient for short call chunks
        _whisper_model = whisper.load_model("tiny")

    return _deepfake_model, _scam_model, _whisper_model


def analyze_audio_file(audio_path):
    """
    Analyzes a single audio file end-to-end.
    Returns a dict with score, color, probabilities, transcript, and
    whether to alert the family.

    audio_path: path to a .wav or .flac file (3 seconds ideal)
    """
    deepfake_model, scam_model, whisper_model = _load_models()

    # --- Step 1: Deepfake voice detection ---
    mfcc = extract_mfcc(audio_path)
    deepfake_prob = predict_deepfake_probability(deepfake_model, mfcc)

    # --- Step 2: Speech to text ---
    result = whisper_model.transcribe(audio_path)
    transcript = result["text"].strip()

    # --- Step 3: Scam language detection ---
    # Use keyword scoring only if DistilBERT model not available
    try:
        scam_prob = scam_model.combined_score(transcript)
    except Exception:
        scam_prob = keyword_score(transcript)

    # --- Step 4: Risk engine ---
    assessment = assess_call_chunk(deepfake_prob, scam_prob)
    assessment["transcript"] = transcript

    return assessment


if __name__ == "__main__":
    # Test on a real file from your ASVspoof dataset
    # LA_T_9999995.flac was confirmed FAKE (label=1) earlier
    test_file = "data/asvspoof2019/LA/ASVspoof2019_LA_train/flac/LA_T_9999995.flac"

    print("Running full pipeline on test file...")
    print(f"File: {test_file}\n")

    result = analyze_audio_file(test_file)

    print("\n--- RESULT ---")
    print(f"Transcript:      '{result['transcript']}'")
    print(f"Deepfake prob:   {result['deepfake_prob']}")
    print(f"Scam lang prob:  {result['scam_language_prob']}")
    print(f"Risk score:      {result['score']}/100")
    print(f"Color:           {result['color']}")
    print(f"Alert family:    {result['alert_family']}")
