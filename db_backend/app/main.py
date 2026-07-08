"""
This is your API server. It wraps every crud.py function in an HTTP route
so the frontend (or Postman, or curl) can reach your database.

Run it with:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for an interactive test page —
FastAPI builds that automatically from this file.
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from .database import get_db, engine, Base

# Creates tables if they don't already exist (safe to leave in — won't
# touch tables/data that already exist).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Bodyguard API")

# Allows your Vue frontend (running on localhost:5173) to call this API.
# Add your deployed frontend URL here too once you host it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Digital Bodyguard API is running"}


# ---------- USERS ----------

@app.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    # NOTE: this stores the raw password as-is for now. Before this goes
    # anywhere real, hash it (e.g. with passlib/bcrypt) instead of storing
    # plain text — fine for local testing, not fine for production.
    return crud.create_user(db, user.name, user.email, user.password, user.phone)


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------- CONTACTS ----------

@app.post("/contacts", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
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


# ---------- CALLS ----------
# save_call_result is the endpoint your friend's model code will hit once
# a call has been analyzed.

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


# ---------- NOTIFICATIONS ----------

@app.post("/notifications", response_model=schemas.NotificationOut)
def create_notification(notif: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return crud.add_notification(db, notif.user_id, notif.message, notif.call_id)


@app.get("/notifications/{user_id}", response_model=List[schemas.NotificationOut])
def list_notifications(user_id: int, db: Session = Depends(get_db)):
    return crud.get_notifications_for_user(db, user_id)


# ---------- SETTINGS ----------

@app.post("/settings", response_model=schemas.SettingOut)
def set_setting(setting: schemas.SettingSet, db: Session = Depends(get_db)):
    return crud.set_setting(db, setting.user_id, setting.key, setting.value)


@app.get("/settings/{user_id}", response_model=List[schemas.SettingOut])
def list_settings(user_id: int, db: Session = Depends(get_db)):
    return crud.get_settings_for_user(db, user_id)
