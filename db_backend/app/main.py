"""
FastAPI application — Digital Bodyguard backend

Run from db_backend/ folder:
    uvicorn app.main:app --reload --port 5000

Then open http://localhost:5000/docs for interactive API docs.
"""
import os
import sys
import tempfile
from typing import List

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db, engine, Base

# Creates all tables on startup
Base.metadata.create_all(bind=engine)

# Load Sarah's pipeline (models load once at startup)
SARAH_BACKEND_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "backend")
sys.path.append(SARAH_BACKEND_PATH)

try:
    from src.pipeline import analyze_audio_file, _load_models
    print("Loading AI models...")
    _load_models()
    print("Models ready.")
    PIPELINE_AVAILABLE = True
except Exception as e:
    print(f"Warning: Could not load pipeline: {e}")
    print("Server will run but /analyze will not work without the model files.")
    PIPELINE_AVAILABLE = False

app = FastAPI(
    title="Digital Bodyguard API",
    description="Real-time scam and deepfake call detection for elderly users",
    version="1.0.0"
)

# Allow Vue frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Root ──────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "Digital Bodyguard API is running"}


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok", "models_loaded": PIPELINE_AVAILABLE}


# ── Auth / Users (original) ───────────────────────────────────────────────────

@app.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user_by_email(db, user.name, user.email, user.password, user.phone)


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ── Contacts (original) ───────────────────────────────────────────────────────

@app.post("/contacts", response_model=schemas.ContactOut)
def add_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.add_contact(db, contact.user_id, contact.name, contact.phone, contact.relation)


@app.get("/contacts/{user_id}", response_model=List[schemas.ContactOut])
def list_contacts(user_id: int, db: Session = Depends(get_db)):
    return crud.get_contacts_for_user(db, user_id)


@app.delete("/contacts/{contact_id}")
def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.delete_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"status": "deleted", "id": contact_id}


# ── Calls (original) ──────────────────────────────────────────────────────────

@app.post("/calls/result", response_model=schemas.CallOut)
def save_call_result(result: schemas.CallResult, db: Session = Depends(get_db)):
    return crud.save_call_result(db, result.user_id, result.verdict, result.confidence, result.caller_number)


@app.get("/calls/{user_id}", response_model=List[schemas.CallOut])
def list_calls(user_id: int, db: Session = Depends(get_db)):
    return crud.get_calls_for_user(db, user_id)


@app.get("/calls/details/{call_id}", response_model=schemas.CallOut)
def call_details(call_id: int, db: Session = Depends(get_db)):
    call = crud.get_call_by_id(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call


# ── Notifications (original) ──────────────────────────────────────────────────

@app.post("/notifications", response_model=schemas.NotificationOut)
def create_notification(notif: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return crud.add_notification(db, notif.user_id, notif.message, notif.call_id)


@app.get("/notifications/{user_id}", response_model=List[schemas.NotificationOut])
def list_notifications(user_id: int, db: Session = Depends(get_db)):
    return crud.get_notifications_for_user(db, user_id)


# ── Settings (original) ───────────────────────────────────────────────────────

@app.post("/settings", response_model=schemas.SettingOut)
def set_setting(setting: schemas.SettingSet, db: Session = Depends(get_db)):
    return crud.set_setting(db, setting.user_id, setting.key, setting.value)


@app.get("/settings/{user_id}", response_model=List[schemas.SettingOut])
def list_settings(user_id: int, db: Session = Depends(get_db)):
    return crud.get_settings_for_user(db, user_id)


# ── Main analysis endpoint (Digital Bodyguard pipeline) ───────────────────────

@app.post("/analyze", response_model=schemas.AnalysisResult)
async def analyze_audio(
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI pipeline not available. Check model files.")

    suffix = os.path.splitext(audio.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = analyze_audio_file(tmp_path)
        crud.save_call_log(db, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ── Call log endpoints ────────────────────────────────────────────────────────

@app.get("/logs", response_model=List[schemas.CallLogResponse])
def get_all_logs(db: Session = Depends(get_db)):
    return crud.get_all_logs(db)


@app.get("/logs/recent", response_model=List[schemas.CallLogResponse])
def get_recent_logs(db: Session = Depends(get_db)):
    return crud.get_recent_logs(db, limit=10)


@app.get("/logs/alerts", response_model=List[schemas.CallLogResponse])
def get_alert_logs(db: Session = Depends(get_db)):
    return crud.get_high_risk_logs(db)


# ── Dashboard stats ───────────────────────────────────────────────────────────

@app.get("/stats", response_model=schemas.StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)