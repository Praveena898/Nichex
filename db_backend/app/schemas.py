"""
Pydantic schemas = the shape of data going in and out of the API.
models.py defines your DATABASE tables.
schemas.py defines what JSON the API accepts and returns.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------- USERS (original auth) ----------

class UserRegister(BaseModel):
    """Used for /auth/register endpoint"""
    name: str
    email: str
    password: str
    phone: Optional[str] = None


class UserOut(BaseModel):
    """Returned by /auth/register and /users/{id}"""
    id: int
    name: str
    email: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- CONTACTS (original) ----------

class ContactCreate(BaseModel):
    user_id: int
    name: str
    phone: str
    relation: Optional[str] = None


class ContactOut(BaseModel):
    id: int
    user_id: int
    name: str
    phone: str
    relation: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- CALLS (original) ----------

class CallResult(BaseModel):
    user_id: int
    verdict: str
    confidence: float
    caller_number: Optional[str] = None


class CallOut(BaseModel):
    id: int
    user_id: int
    caller_number: Optional[str] = None
    verdict: str
    confidence: float
    started_at: datetime

    class Config:
        from_attributes = True


# ---------- NOTIFICATIONS (original) ----------

class NotificationCreate(BaseModel):
    user_id: int
    message: str
    call_id: Optional[int] = None


class NotificationOut(BaseModel):
    id: int
    user_id: int
    call_id: Optional[int] = None
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- SETTINGS (original) ----------

class SettingSet(BaseModel):
    user_id: int
    key: str
    value: str


class SettingOut(BaseModel):
    id: int
    user_id: int
    key: str
    value: str

    class Config:
        from_attributes = True


# ── Digital Bodyguard schemas ─────────────────────────────────────────────────

class CallLogCreate(BaseModel):
    user_id:       int = 1
    timestamp:     str
    risk_score:    int
    color:         str
    deepfake_prob: float
    scam_prob:     float
    transcript:    Optional[str] = None
    alert_sent:    bool = False
    chunk_num:     int = 0


class CallLogResponse(BaseModel):
    log_id:        int
    user_id:       int
    timestamp:     str
    risk_score:    int
    color:         str
    deepfake_prob: float
    scam_prob:     float
    transcript:    Optional[str]
    alert_sent:    bool
    chunk_num:     int

    class Config:
        from_attributes = True


class AnalysisResult(BaseModel):
    """Exactly matches what analyze_audio_file() returns from Sarah's pipeline"""
    score:              int
    color:              str
    deepfake_prob:      float
    deepfake_prob_raw:  Optional[float] = None
    scam_language_prob: float
    transcript:         Optional[str] = None
    transcript_confidence: Optional[float] = None
    alert_family:       bool
    chunk_num:          Optional[int] = 0


class StatsResponse(BaseModel):
    total_chunks_analyzed: int
    red_alerts:            int
    yellow_warnings:       int
    safe_chunks:           int
    family_alerts_sent:    int
    average_risk_score:    float


class UserCreate(BaseModel):
    """Used for Digital Bodyguard /users endpoint"""
    name:         str
    phone_number: str
    app_language: str = "English"


class UserResponse(BaseModel):
    user_id:            int
    name:               str
    phone_number:       str
    monitoring_enabled: bool

    class Config:
        from_attributes = True


class EmergencyContactCreate(BaseModel):
    user_id:      int
    name:         str
    phone_number: str
    relationship: Optional[str] = None


class EmergencyContactResponse(BaseModel):
    contact_id:   int
    user_id:      int
    name:         str
    phone_number: str
    relationship: Optional[str]

    class Config:
        from_attributes = True

# Alias so main.py can use either name
ContactResponse = EmergencyContactResponse