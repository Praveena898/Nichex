"""
The full Digital Bodyguard pipeline — connects both trained models into
one function you call with an audio file and get back a real risk assessment.

Flow:
    audio file (.flac/.wav/.m4a/.opus)
        ↓
    MFCC extractor → Deepfake CNN → deepfake_prob
        ↓
    Whisper STT → language detection
        ↓
    Scam NLP
        ├── English → DistilBERT
        ├── Hindi/Tamil/Malayalam → MuRIL
        └── Mixed language → BOTH models → higher probability
        ↓
    Risk Engine → score + color + alert_family
"""

import os
import sys
from pathlib import Path

import whisper

# Make backend available for imports
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from src.features.mfcc_extractor import (
    extract_mfcc
)

from src.features.transcription import (
    transcribe_with_whisper,
    WHISPER_MODEL_NAME
)

from src.models.deepfake_cnn import (
    load_deepfake_model,
    predict_deepfake_probability
)

from src.models.scam_nlp import (
    ScamNLPModel,
    keyword_score
)

from src.risk_engine import (
    assess_call_chunk
)


# =========================================================
# MODEL PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEEPFAKE_MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "deepfake_cnn.pth"
)

ENGLISH_MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "scam_distilbert"
)

MURIL_MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "scam_muril"
)


# =========================================================
# MODEL CACHE
# =========================================================

_deepfake_model = None
_english_model = None
_muril_model = None
_whisper_model = None


# =========================================================
# LOAD MODELS
# =========================================================

def _load_models():
    """Lazy-load all models. Models are loaded only once."""

    global _deepfake_model, _english_model, _muril_model, _whisper_model

    if _deepfake_model is None:
        print("Loading deepfake CNN model...")
        _deepfake_model = load_deepfake_model(
            DEEPFAKE_MODEL_PATH
        )

    if _english_model is None:
        print("Loading English DistilBERT...")
        _english_model = ScamNLPModel(
            model_path=ENGLISH_MODEL_PATH
        )

    if _muril_model is None:
        print("Loading MuRIL...")
        _muril_model = ScamNLPModel(
            model_path=MURIL_MODEL_PATH
        )

    if _whisper_model is None:
        print(
            f"Loading Whisper speech-to-text model "
            f"({WHISPER_MODEL_NAME})..."
        )
        _whisper_model = whisper.load_model(
            WHISPER_MODEL_NAME
        )

    return (
        _deepfake_model,
        _english_model,
        _muril_model,
        _whisper_model
    )
# =========================================================
# MIXED LANGUAGE DETECTION
# =========================================================

def is_mixed_language(text):
    """
    Detect whether the transcript contains both:

        1. English/Latin characters
        2. Indian-language characters

    Supported Indian scripts:

        Hindi      → Devanagari
        Tamil      → Tamil
        Malayalam  → Malayalam

    Examples:

        "Hello कृपया OTP बताइए"
            → True

        "Hello வணக்கம்"
            → True

        "Hello നിങ്ങളുടെ ബാങ്ക്"
            → True

        "Hello please verify my account"
            → False

        "कृपया अपना OTP बताइए"
            → False
    """

    has_english_script = False
    has_indian_script = False

    for ch in text:

        code = ord(ch)

        # -------------------------------------------------
        # Hindi / Devanagari
        # -------------------------------------------------

        if 0x0900 <= code <= 0x097F:

            has_indian_script = True

        # -------------------------------------------------
        # Tamil
        # -------------------------------------------------

        elif 0x0B80 <= code <= 0x0BFF:

            has_indian_script = True

        # -------------------------------------------------
        # Malayalam
        # -------------------------------------------------

        elif 0x0D00 <= code <= 0x0D7F:

            has_indian_script = True

        # -------------------------------------------------
        # English / Latin alphabet
        # -------------------------------------------------

        elif ch.isascii() and ch.isalpha():

            has_english_script = True

    return (
        has_english_script
        and has_indian_script
    )


# =========================================================
# ANALYZE AUDIO
# =========================================================

def analyze_audio_file(audio_path):

    """
    Analyzes a single audio file end-to-end.

    Returns:

        risk score
        risk color
        deepfake probability
        scam language probability
        transcript
        transcript confidence
        detected language
    """

    # -----------------------------------------------------
    # Load all models
    # -----------------------------------------------------

    (
        deepfake_model,
        english_model,
        muril_model,
        whisper_model
    ) = _load_models()


    # =====================================================
    # STEP 1 — DEEPFAKE VOICE DETECTION
    # =====================================================

    mfcc = extract_mfcc(
        audio_path
    )

    deepfake_prob = predict_deepfake_probability(
        deepfake_model,
        mfcc
    )


    # =====================================================
    # STEP 2 — WHISPER SPEECH-TO-TEXT
    # =====================================================

    (
        transcript,
        transcript_confidence,
        language
    ) = transcribe_with_whisper(
        whisper_model,
        audio_path
    )

    print(
        f"Detected language: {language}"
    )


    # =====================================================
    # STEP 3 — SCAM LANGUAGE DETECTION
    # =====================================================

    if (
        transcript_confidence < 0.35
        or len(transcript.strip()) < 2
    ):

        # Whisper failed or transcript is unreliable

        scam_prob = 0.0

    else:

        # -------------------------------------------------
        # Rule-based keyword detector
        # -------------------------------------------------

        keyword_prob = keyword_score(
            transcript
        )

        try:

            # =================================================
            # CASE 1 — MIXED LANGUAGE
            # =================================================

            if is_mixed_language(transcript):

                print(
                    "Mixed language detected"
                )

                # Run BOTH models

                english_prob = (
                    english_model
                    .combined_score(transcript)
                )

                muril_prob = (
                    muril_model
                    .combined_score(transcript)
                )

                print(
                    f"English DistilBERT probability: "
                    f"{english_prob:.2f}"
                )

                print(
                    f"MuRIL probability: "
                    f"{muril_prob:.2f}"
                )

                # Take the stronger detector

                bert_prob = max(
                    english_prob,
                    muril_prob
                )


            # =================================================
            # CASE 2 — ENGLISH
            # =================================================

            elif language.startswith("en"):

                print(
                    "Using English DistilBERT"
                )

                bert_prob = (
                    english_model
                    .combined_score(transcript)
                )


            # =================================================
            # CASE 3 — INDIAN / OTHER LANGUAGE
            # =================================================

            else:

                print(
                    f"Using MuRIL ({language})"
                )

                bert_prob = (
                    muril_model
                    .combined_score(transcript)
                )


            # -------------------------------------------------
            # Combine NLP + keyword detector
            # -------------------------------------------------

            scam_prob = max(
                bert_prob,
                keyword_prob
            )


            # -------------------------------------------------
            # Whisper confidence adjustment
            # -------------------------------------------------

            if transcript_confidence < 0.35:

                scam_prob = keyword_prob

            elif transcript_confidence < 0.55:

                scam_prob *= 0.90


        except Exception as e:

            print(
                f"NLP model error: {e}"
            )

            # Fall back to keyword detector

            scam_prob = (
                keyword_prob
                * transcript_confidence
            )


        # =================================================
        # KEYWORD BOOST
        # =================================================

        if keyword_prob >= 0.67:

            scam_prob = min(
                1.0,
                scam_prob + 0.20
            )


    # =====================================================
    # STEP 4 — DEEPFAKE ADJUSTMENT
    # =====================================================

    deepfake_prob_raw = deepfake_prob

    # If speech is very clear and scam probability
    # is very low, reduce possible false deepfake alarm.

    if (
        transcript_confidence >= 0.75
        and scam_prob < 0.20
    ):

        deepfake_prob *= 0.45


    # =====================================================
    # STEP 5 — FINAL RISK ASSESSMENT
    # =====================================================

    assessment = assess_call_chunk(
        deepfake_prob,
        scam_prob,
        transcript
    )


    # =====================================================
    # ADD EXTRA INFORMATION
    # =====================================================

    assessment["deepfake_prob_raw"] = round(
        deepfake_prob_raw,
        2
    )

    assessment["deepfake_prob"] = round(
        deepfake_prob,
        2
    )

    assessment["scam_language_prob"] = round(
        scam_prob,
        2
    )

    assessment["transcript"] = transcript

    assessment["transcript_confidence"] = round(
        transcript_confidence,
        2
    )

    assessment["language"] = language


    return assessment


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    test_file = (
        "data/asvspoof2019/"
        "LA/ASVspoof2019_LA_train/flac/"
        "LA_T_9999995.flac"
    )

    print(
        "Running full pipeline on test file..."
    )

    print(
        f"File: {test_file}\n"
    )

    result = analyze_audio_file(
        test_file
    )

    print(
        "\n--- RESULT ---"
    )

    print(
        f"Transcript:      "
        f"'{result['transcript']}'"
    )

    print(
        f"Language:        "
        f"{result.get('language')}"
    )

    print(
        f"Transcript conf: "
        f"{result.get('transcript_confidence')}"
    )

    print(
        f"Deepfake prob:   "
        f"{result['deepfake_prob']}"
    )

    print(
        f"Scam lang prob:  "
        f"{result['scam_language_prob']}"
    )

    print(
        f"Risk score:      "
        f"{result['score']}/100"
    )

    print(
        f"Color:           "
        f"{result['color']}"
    )

    print(
        f"Alert family:    "
        f"{result['alert_family']}"
    )