"""
Run this ONE file to create your database and tables:

    python init_db.py

It will:
 1. Create digital_bodyguard.db (if it doesn't exist)
 2. Create all 5 tables inside it
 3. Insert a couple of sample rows so you have something to look at
    in DB Browser for SQLite
"""
from app.database import engine, SessionLocal, Base
from app import models, crud

# Step 1 + 2: create the .db file and all tables defined in models.py
Base.metadata.create_all(bind=engine)
print("Tables created in digital_bodyguard.db")

# Step 3: insert sample/dummy data so you can see it working
db = SessionLocal()

existing = crud.get_user_by_email(db, "praveena@example.com")
if not existing:
    user = crud.create_user(
        db,
        name="Praveena",
        email="praveena@example.com",
        password_hash="dummy_hash_for_now",   # real hashing comes in the auth step
        phone="9999999999",
    )
    crud.add_contact(db, user.id, name="Mom", phone="9876543210", relation="Mother")
    crud.add_contact(db, user.id, name="Brother", phone="9876500000", relation="Brother")

    call = crud.save_call_result(db, user.id, verdict="scam", confidence=0.91, caller_number="+911234567890")
    crud.add_notification(db, user.id, message="Scam call detected and blocked.", call_id=call.id)

    crud.set_setting(db, user.id, key="notifications_enabled", value="true")

    print(f"Sample user created: id={user.id}, email={user.email}")
else:
    print("Sample user already exists, skipping insert.")

db.close()
print("Done. Open digital_bodyguard.db in DB Browser for SQLite to see it.")
