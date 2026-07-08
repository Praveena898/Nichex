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
