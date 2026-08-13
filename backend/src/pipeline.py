"""
The full Digital Bodyguard pipeline — connects both trained models into
one function you call with an audio file and get back a real risk assessment.

Flow:
    audio file (.flac/.wav/.m4a)
        ↓
    mfcc_extractor  →  deepfake_cnn  →  deepfake_prob (real)
        ↓
    whisper STT  →  scam_nlp  →  scam_language_prob (real)
        ↓
    risk_engine  →  score + color + alert_family (real)
"""

import os
import sys
from pathlib import Path

import whisper

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.features.mfcc_extractor import extract_mfcc
from src.features.transcription import transcribe_with_whisper, WHISPER_MODEL_NAME
from src.models.deepfake_cnn import load_deepfake_model, predict_deepfake_probability
from src.models.scam_nlp import ScamNLPModel, keyword_score
from src.risk_engine import assess_call_chunk

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEEPFAKE_MODEL_PATH = PROJECT_ROOT / "backend" / "models" / "deepfake_cnn.pth"
SCAM_MODEL_PATH = PROJECT_ROOT / "backend" / "models" / "scam_distilbert"

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
        print(f"Loading Whisper speech-to-text model ({WHISPER_MODEL_NAME})...")
        _whisper_model = whisper.load_model(WHISPER_MODEL_NAME)

    return _deepfake_model, _scam_model, _whisper_model


def analyze_audio_file(audio_path):
    """
    Analyzes a single audio file end-to-end.
    Returns:
        - risk score
        - color
        - deepfake probability
        - scam language probability
        - transcript
        - transcript confidence
    """

    deepfake_model, scam_model, whisper_model = _load_models()

    # ---------------------------------------------------------
    # Step 1: Deepfake Voice Detection
    # ---------------------------------------------------------
    mfcc = extract_mfcc(audio_path)
    deepfake_prob = predict_deepfake_probability(deepfake_model, mfcc)

    # ---------------------------------------------------------
    # Step 2: Speech-to-Text
    # ---------------------------------------------------------
    transcript, transcript_confidence = transcribe_with_whisper(
        whisper_model,
        audio_path
    )

    # ---------------------------------------------------------
    # Step 3: Scam Language Detection
    # ---------------------------------------------------------
    if transcript_confidence < 0.35 or len(transcript.strip()) < 2:
        # Whisper failed or transcript unreliable
        scam_prob = 0.0

    else:

        # Rule-based keyword score (0-1)
        keyword_prob = keyword_score(transcript)

        try:
            # DistilBERT prediction
            bert_prob = scam_model.combined_score(transcript)

            # Use whichever detector is more confident
            scam_prob = max(bert_prob, keyword_prob)

            # Adjust using Whisper confidence
            scam_prob *= transcript_confidence

        except Exception:
            scam_prob = keyword_prob * transcript_confidence

        # -----------------------------------------------------
        # Keyword Boost
        # If 2 or more scam keywords appear,
        # raise suspicion slightly.
        # -----------------------------------------------------
        if keyword_prob >= 0.67:
            scam_prob = min(1.0, scam_prob + 0.20)

    # ---------------------------------------------------------
    # Step 4: Deepfake Adjustment
    # ---------------------------------------------------------
    deepfake_prob_raw = deepfake_prob

    # If transcript is very clear and language is harmless,
    # reduce false deepfake alarms.
    if transcript_confidence >= 0.75 and scam_prob < 0.20:
        deepfake_prob *= 0.45

    # ---------------------------------------------------------
    # Step 5: Final Risk Assessment
    # ---------------------------------------------------------
    assessment = assess_call_chunk(deepfake_prob, scam_prob,transcript)

    assessment["deepfake_prob_raw"] = round(deepfake_prob_raw, 2)
    assessment["deepfake_prob"] = round(deepfake_prob, 2)
    assessment["scam_language_prob"] = round(scam_prob, 2)
    assessment["transcript"] = transcript
    assessment["transcript_confidence"] = round(transcript_confidence, 2)

    return assessment

if __name__ == "__main__":
    test_file = "data/asvspoof2019/LA/ASVspoof2019_LA_train/flac/LA_T_9999995.flac"

    print("Running full pipeline on test file...")
    print(f"File: {test_file}\n")

    result = analyze_audio_file(test_file)

    print("\n--- RESULT ---")
    print(f"Transcript:      '{result['transcript']}'")
    print(f"Transcript conf: {result.get('transcript_confidence')}")
    print(f"Deepfake prob:   {result['deepfake_prob']}")
    print(f"Scam lang prob:  {result['scam_language_prob']}")
    print(f"Risk score:      {result['score']}/100")
    print(f"Color:           {result['color']}")
    print(f"Alert family:    {result['alert_family']}")
