"""
This file defines all database tables as Python classes.
Each class = one table. Each Column = one column in that table.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


# ── Original tables ───────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    email         = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone         = Column(String)
    created_at    = Column(DateTime, default=datetime.utcnow)

    # original relationships
    contacts      = relationship("Contact", back_populates="owner")
    calls         = relationship("Call", back_populates="owner")
    notifications = relationship("Notification", back_populates="owner")
    settings      = relationship("Setting", back_populates="owner")

    # Digital Bodyguard relationships
    call_logs          = relationship("CallLog", back_populates="user")
    emergency_contacts = relationship("EmergencyContact", back_populates="user")


class Contact(Base):
    __tablename__ = "contacts"

    id       = Column(Integer, primary_key=True, index=True)
    user_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    name     = Column(String, nullable=False)
    phone    = Column(String, nullable=False)
    relation = Column(String)

    owner = relationship("User", back_populates="contacts")


class Call(Base):
    __tablename__ = "calls"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    caller_number = Column(String)
    verdict       = Column(String)
    confidence    = Column(Float)
    started_at    = Column(DateTime, default=datetime.utcnow)
    ended_at      = Column(DateTime, nullable=True)

    owner         = relationship("User", back_populates="calls")
    notifications = relationship("Notification", back_populates="call")


class Notification(Base):
    __tablename__ = "notifications"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    call_id    = Column(Integer, ForeignKey("calls.id"), nullable=True)
    message    = Column(String, nullable=False)
    is_read    = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="notifications")
    call  = relationship("Call", back_populates="notifications")


class Setting(Base):
    __tablename__ = "settings"

    id      = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key     = Column(String, nullable=False)
    value   = Column(String, nullable=False)

    owner = relationship("User", back_populates="settings")


# ── Digital Bodyguard tables ──────────────────────────────────────────────────

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    contact_id    = Column(Integer, primary_key=True, autoincrement=True)
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    name          = Column(String(100), nullable=False)
    phone_number  = Column(String(15), nullable=False)
    relation_type = Column(String(50))   # renamed from 'relationship' to avoid conflict
    added_at      = Column(String, nullable=False)

    user   = relationship("User", back_populates="emergency_contacts")
    alerts = relationship("FamilyAlert", back_populates="contact")


class CallLog(Base):
    __tablename__ = "call_logs"

    log_id        = Column(Integer, primary_key=True, autoincrement=True)
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp     = Column(String, nullable=False)
    risk_score    = Column(Integer, nullable=False)
    color         = Column(String(10), nullable=False)
    deepfake_prob = Column(Float, nullable=False)
    scam_prob     = Column(Float, nullable=False)
    transcript    = Column(Text, nullable=True)
    alert_sent    = Column(Boolean, default=False)
    chunk_num     = Column(Integer, default=0)

    user  = relationship("User", back_populates="call_logs")
    alert = relationship("FamilyAlert", back_populates="call_log", uselist=False)


class FamilyAlert(Base):
    __tablename__ = "family_alerts"

    alert_id   = Column(Integer, primary_key=True, autoincrement=True)
    log_id     = Column(Integer, ForeignKey("call_logs.log_id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("emergency_contacts.contact_id"), nullable=False)
    sent_at    = Column(String, nullable=False)
    status     = Column(String(10), default="sent")

    call_log = relationship("CallLog", back_populates="alert")
    contact  = relationship("EmergencyContact", back_populates="alerts")