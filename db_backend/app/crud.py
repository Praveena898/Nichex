"""
CRUD = Create, Read, Update, Delete.
This file has one small function per action. Your API routes will
just call these functions instead of writing raw database code everywhere.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from . import models, schemas
from .auth import verify_password, hash_password


# ---------- USERS (original) ----------

def create_user_by_email(db: Session, name: str, email: str, password: str, phone: str = None):
    """Create user with a properly hashed password."""
    hashed_password = hash_password(password)

    user = models.User(
        name=name,
        email=email,
        password_hash=hashed_password,
        phone=phone
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------- CONTACTS (original) ----------

def add_contact(db: Session, user_id: int, name: str, phone: str, relation: str = None):
    contact = models.Contact(user_id=user_id, name=name, phone=phone, relation=relation)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contacts_for_user(db: Session, user_id: int):
    return db.query(models.Contact).filter(models.Contact.user_id == user_id).all()


def delete_contact(db: Session, contact_id: int):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


# ---------- CALLS (original) ----------

def save_call_result(db: Session, user_id: int, verdict: str, confidence: float, caller_number: str = None):
    call = models.Call(
        user_id=user_id,
        caller_number=caller_number,
        verdict=verdict,
        confidence=confidence,
    )
    db.add(call)
    db.commit()
    db.refresh(call)
    return call


def get_calls_for_user(db: Session, user_id: int):
    return db.query(models.Call).filter(models.Call.user_id == user_id).order_by(models.Call.started_at.desc()).all()


def get_call_by_id(db: Session, call_id: int):
    return db.query(models.Call).filter(models.Call.id == call_id).first()


# ---------- NOTIFICATIONS (original) ----------

def add_notification(db: Session, user_id: int, message: str, call_id: int = None):
    notif = models.Notification(user_id=user_id, message=message, call_id=call_id)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def get_notifications_for_user(db: Session, user_id: int):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).order_by(models.Notification.created_at.desc()).all()


# ---------- SETTINGS (original) ----------

def set_setting(db: Session, user_id: int, key: str, value: str):
    setting = db.query(models.Setting).filter(
        models.Setting.user_id == user_id, models.Setting.key == key
    ).first()
    if setting:
        setting.value = value
    else:
        setting = models.Setting(user_id=user_id, key=key, value=value)
        db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def get_settings_for_user(db: Session, user_id: int):
    return db.query(models.Setting).filter(models.Setting.user_id == user_id).all()


# ── CallLog CRUD (Digital Bodyguard pipeline) ─────────────────────────────────

def save_call_log(db: Session, result: dict, user_id: int)-> models.CallLog:
    """
    Saves one pipeline result to the database.
    result = the dict returned by Sarah's analyze_audio_file()
    """
    log = models.CallLog(
        user_id       = user_id,
        timestamp     = datetime.now().isoformat(),
        risk_score    = result.get("score", 0),
        color         = result.get("color", "GREEN"),
        deepfake_prob = result.get("deepfake_prob", 0.0),
        scam_prob     = result.get("scam_language_prob", 0.0),
        transcript    = result.get("transcript", ""),
        alert_sent    = result.get("alert_family", False),
        chunk_num     = result.get("chunk_num", 0)
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_all_logs(db: Session) -> list:
    return db.query(models.CallLog).order_by(models.CallLog.log_id.desc()).all()


def get_recent_logs(db: Session, limit: int = 10) -> list:
    return db.query(models.CallLog).order_by(models.CallLog.log_id.desc()).limit(limit).all()


def get_high_risk_logs(db: Session) -> list:
    return db.query(models.CallLog).filter(models.CallLog.color == "RED").order_by(models.CallLog.log_id.desc()).all()


def get_stats(db: Session) -> dict:
    total     = db.query(func.count(models.CallLog.log_id)).scalar() or 0
    red       = db.query(func.count(models.CallLog.log_id)).filter(models.CallLog.color == "RED").scalar() or 0
    yellow    = db.query(func.count(models.CallLog.log_id)).filter(models.CallLog.color == "YELLOW").scalar() or 0
    green     = db.query(func.count(models.CallLog.log_id)).filter(models.CallLog.color == "GREEN").scalar() or 0
    alerts    = db.query(func.count(models.CallLog.log_id)).filter(models.CallLog.alert_sent == True).scalar() or 0
    avg_score = db.query(func.avg(models.CallLog.risk_score)).scalar() or 0.0
    return {
        "total_chunks_analyzed": total,
        "red_alerts":            red,
        "yellow_warnings":       yellow,
        "safe_chunks":           green,
        "family_alerts_sent":    alerts,
        "average_risk_score":    round(float(avg_score), 1)
    }


# ── User CRUD (Digital Bodyguard) ─────────────────────────────────────────────

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        name           = user.name,
        phone_number   = user.phone_number,
        app_language   = user.app_language,
        created_at     = datetime.now().isoformat()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


# ── EmergencyContact CRUD ─────────────────────────────────────────────────────

def create_contact(db: Session, contact: schemas.ContactCreate) -> models.EmergencyContact:
    db_contact = models.EmergencyContact(
        user_id       = contact.user_id,
        name          = contact.name,
        phone_number  = contact.phone_number,
        relation_type = contact.relationship,
        added_at      = datetime.now().isoformat()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts_by_user(db: Session, user_id: int) -> list:
    return db.query(models.EmergencyContact).filter(models.EmergencyContact.user_id == user_id).all()

def get_logs_for_user(db: Session, user_id: int):
    return (
        db.query(models.CallLog)
        .filter(models.CallLog.user_id == user_id)
        .order_by(models.CallLog.log_id.desc())
        .all()
    )