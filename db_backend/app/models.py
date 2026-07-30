"""
This file defines your 5 tables as Python classes.
Each class = one table. Each Column = one column in that table.
This IS your Stage 1 design, just written in SQLAlchemy instead of on paper.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # these let you do user.contacts, user.calls, etc. in Python
    contacts = relationship("Contact", back_populates="owner")
    calls = relationship("Call", back_populates="owner")
    notifications = relationship("Notification", back_populates="owner")
    settings = relationship("Setting", back_populates="owner")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    relation = Column(String)  # e.g. "Daughter", "Son", "Neighbor"

    owner = relationship("User", back_populates="contacts")


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    caller_number = Column(String)
    verdict = Column(String)       # "safe" | "suspicious" | "scam"
    confidence = Column(Float)     # 0.0 to 1.0, filled in by the ML model later
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="calls")
    notifications = relationship("Notification", back_populates="call")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=True)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="notifications")
    call = relationship("Call", back_populates="notifications")


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String, nullable=False)     # e.g. "notifications_enabled"
    value = Column(String, nullable=False)   # store as text, e.g. "true"

    owner = relationship("User", back_populates="settings")

# app/main.py
# FastAPI application — Digital Bodyguard backend
#
# Run from db_backend/ folder:
#   uvicorn app.main:app --reload --port 5000
#
# API docs available at: http://localhost:5000/docs

import os
import sys
import tempfile
from typing import List

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Allow importing Sarah's pipeline from the Nichex/backend/ folder
# Praveena: update this path to point to where Sarah's code is on your machine
SARAH_BACKEND_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "backend")
sys.path.append(SARAH_BACKEND_PATH)

from .database import engine, Base, get_db
from . import models, crud, schemas

# Create all tables on startup
Base.metadata.create_all(bind=engine)

# Load Sarah's pipeline (models load once at startup)
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

# Allow Vue.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "models_loaded": PIPELINE_AVAILABLE
    }


# ── Main analysis endpoint ────────────────────────────────────────────────────

@app.post("/analyze", response_model=schemas.AnalysisResult)
async def analyze_audio(
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Receives an audio file from Vue frontend.
    Runs Sarah's full pipeline (deepfake CNN + scam NLP + risk engine).
    Saves result to database.
    Returns risk score, color, transcript to Vue.
    """
    if not PIPELINE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AI pipeline not available. Check model files."
        )

    # Save uploaded file to temp location
    suffix = os.path.splitext(audio.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Run Sarah's pipeline
        result = analyze_audio_file(tmp_path)

        # Save to database
        crud.save_call_log(db, result)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Always delete temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ── Call history endpoints ────────────────────────────────────────────────────

@app.get("/logs", response_model=List[schemas.CallLogResponse])
def get_all_logs(db: Session = Depends(get_db)):
    """Returns all call logs from database, newest first"""
    return crud.get_all_logs(db)


@app.get("/logs/recent", response_model=List[schemas.CallLogResponse])
def get_recent_logs(db: Session = Depends(get_db)):
    """Returns the 10 most recent call logs"""
    return crud.get_recent_logs(db, limit=10)


@app.get("/logs/alerts", response_model=List[schemas.CallLogResponse])
def get_alert_logs(db: Session = Depends(get_db)):
    """Returns only RED alert logs"""
    return crud.get_high_risk_logs(db)


# ── Dashboard stats ───────────────────────────────────────────────────────────

@app.get("/stats", response_model=schemas.StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Returns dashboard statistics for Vue frontend"""
    return crud.get_stats(db)


# ── User endpoints ────────────────────────────────────────────────────────────

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ── Emergency contact endpoints ───────────────────────────────────────────────

@app.post("/contacts", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@app.get("/contacts/{user_id}", response_model=List[schemas.ContactResponse])
def get_contacts(user_id: int, db: Session = Depends(get_db)):
    return crud.get_contacts_by_user(db, user_id)
