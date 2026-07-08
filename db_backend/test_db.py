"""
Run this AFTER init_db.py to prove reading works too:

    python test_db.py
"""
from app.database import SessionLocal
from app import crud

db = SessionLocal()

user = crud.get_user_by_email(db, "praveena@example.com")
print(f"\nUser: {user.name} ({user.email})")

contacts = crud.get_contacts_for_user(db, user.id)
print(f"Contacts ({len(contacts)}):")
for c in contacts:
    print(f"  - {c.name} ({c.relation}): {c.phone}")

calls = crud.get_calls_for_user(db, user.id)
print(f"Calls ({len(calls)}):")
for call in calls:
    print(f"  - verdict={call.verdict}, confidence={call.confidence}, from={call.caller_number}")

notifications = crud.get_notifications_for_user(db, user.id)
print(f"Notifications ({len(notifications)}):")
for n in notifications:
    print(f"  - {n.message} (read={n.is_read})")

db.close()
