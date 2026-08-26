"""
Live call analysis endpoint.

Receives a short audio chunk from the frontend's mic recorder, converts it
to a format the ML pipeline can read, runs it through the deepfake +
scam-language pipeline, saves the result to the database, and returns
JSON in the exact shape LiveMonitorView.vue expects.
"""
import os
import subprocess
import tempfile
import uuid

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import crud

# ---------------------------------------------------------------------
# IMPORTANT: this import points at your teammate's ML pipeline code.
# Confirm the exact module path and function name/signature with her —
# this assumes a function that takes an audio file path and returns a
# dict with deepfake_prob, scam_language_prob, and transcript.
#
# If backend/ and db_backend/ are sibling folders (not installed as a
# package), you need the sys.path line below so Python can find it.
# ---------------------------------------------------------------------
import sys
BACKEND_SRC_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "backend", "src")
sys.path.insert(0, os.path.abspath(BACKEND_SRC_PATH))

try:
    from pipeline import analyze_audio_file  # noqa: E402
    from risk_engine import calculate_risk_score, get_risk_color  # noqa: E402
except ImportError:
    # Fallback so this file can still be imported/tested before the
    # real pipeline is wired in. Replace this block once the import
    # above works — ask your teammate for the exact function names.
    def analyze_audio_file(path: str):
        raise RuntimeError(
            "Could not import the ML pipeline. Confirm the real module "
            "path/function name with your teammate and update the import "
            "at the top of analyze.py."
        )

    def calculate_risk_score(deepfake_prob, scam_language_prob,
                              deepfake_weight=0.5, scam_weight=0.5):
        return round((deepfake_weight * deepfake_prob
                      + scam_weight * scam_language_prob) * 100)

    def get_risk_color(score):
        if score < 40:
            return "GREEN"
        elif score < 70:
            return "YELLOW"
        return "RED"


router = APIRouter()


def convert_to_wav(input_path: str) -> str:
    """
    The browser's MediaRecorder produces .webm audio. Most speech/audio
    models (Whisper, librosa-based feature extraction) expect .wav.
    This shells out to ffmpeg to convert, matching what your teammate's
    backend already ships (see the ffmpeg folder in backend/).
    """
    output_path = input_path.rsplit(".", 1)[0] + ".wav"
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed: {result.stderr}")
    return output_path


@router.post("/live-analyze")
async def analyze_chunk(
    audio: UploadFile = File(...),
    user_id: int = Form(1),  # default to 1 for demo; wire up real auth later
    caller_number: str = Form(None),
    db: Session = Depends(get_db),
):
    # 1. Save the uploaded chunk to a temp file
    tmp_dir = tempfile.gettempdir()
    raw_path = os.path.join(tmp_dir, f"{uuid.uuid4().hex}_{audio.filename}")
    with open(raw_path, "wb") as f:
        f.write(await audio.read())

    try:
        # 2. Convert webm -> wav for the model pipeline
        wav_path = convert_to_wav(raw_path)

        # 3. Run the ML pipeline
        try:
            result = analyze_audio_file(wav_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model inference failed: {e}")

        deepfake_prob = float(result.get("deepfake_prob", 0.0))
        scam_prob = float(result.get("scam_language_prob", 0.0))
        transcript = result.get("transcript", "")

        # 4. Compute the combined risk score + color
        score = calculate_risk_score(deepfake_prob, scam_prob)
        color = get_risk_color(score)

        # Risk escalation, matching the write-up in the report
        if deepfake_prob >= 0.8:
            score = max(score, 90)
            color = get_risk_color(score)

        # 5. Save this chunk's result to the database
        verdict = color.lower()
        crud.save_call_result(
            db, user_id=user_id, verdict=verdict,
            confidence=score / 100, caller_number=caller_number,
        )

        # 6. Return exactly what LiveMonitorView.vue expects
        return {
            "score": score,
            "color": color,
            "deepfake_prob": deepfake_prob,
            "scam_language_prob": scam_prob,
            "transcript": transcript,
        }

    finally:
        # Clean up temp files either way
        for p in (raw_path, raw_path.rsplit(".", 1)[0] + ".wav"):
            if os.path.exists(p):
                os.remove(p)
