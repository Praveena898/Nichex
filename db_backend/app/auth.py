"""
Handles two things:
  1. Password hashing — so we never store a real password in the database,
     only a scrambled, one-way version of it.
  2. JWT tokens — a signed "ID card" the API hands back after a successful
     login, which the frontend then attaches to future requests to prove
     who's logged in (used later, e.g. for /calls, /contacts per-user).
"""
import bcrypt
from jose import jwt
from datetime import datetime, timedelta

# In a real deployed app this must be a long random secret kept out of your
# code (e.g. in a .env file). Fine to leave as-is for local/college project use.
SECRET_KEY = "digital-bodyguard-dev-secret-change-this-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # token stays valid for 1 day


def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user_id: int, email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "email": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)