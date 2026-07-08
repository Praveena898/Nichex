"""
CRUD = Create, Read, Update, Delete.
This file has one small function per action. Your API routes (later) will
just call these functions instead of writing raw database code everywhere.

You can test every function in this file directly, with no frontend,
no API, nothing else needed. See test_db.py for examples.
"""
from sqlalchemy.orm import Session
from . import models


# ---------- USERS ----------

def create_user(db: Session, name: str, email: str, password_hash: str, phone: str = None):
    user = models.User(name=name, email=email, password_hash=password_hash, phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)  # refreshes 'user' so it now has its generated id
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------- CONTACTS ----------

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


# ---------- CALLS ----------
# NOTE: save_call_result() is the ONE function your teammate's real-time/model
# code will call once the ML model finishes analyzing a call. This is the
# entire connection point between your database work and their real-time work.

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


# ---------- NOTIFICATIONS ----------

def add_notification(db: Session, user_id: int, message: str, call_id: int = None):
    notif = models.Notification(user_id=user_id, message=message, call_id=call_id)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def get_notifications_for_user(db: Session, user_id: int):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).order_by(models.Notification.created_at.desc()).all()


# ---------- SETTINGS ----------

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
