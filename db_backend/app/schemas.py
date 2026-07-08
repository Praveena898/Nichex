"""
Pydantic schemas = the "shape" of data going in and out of the API.
models.py defines your DATABASE tables.
schemas.py defines what JSON the API accepts and returns.
They look similar but serve different jobs — this is normal in FastAPI projects.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------- USERS ----------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True  # lets this read straight from a SQLAlchemy model


# ---------- CONTACTS ----------

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


# ---------- CALLS ----------

class CallResult(BaseModel):
    user_id: int
    verdict: str          # "safe" | "suspicious" | "scam"
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


# ---------- NOTIFICATIONS ----------

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


# ---------- SETTINGS ----------

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
