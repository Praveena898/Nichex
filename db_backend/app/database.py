"""
Database connection setup.
This is the file that says "where is our database and how do we talk to it".
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This creates a file called digital_bodyguard.db in your project folder.
# That file IS your database. You can open it directly in "DB Browser for SQLite".
SQLALCHEMY_DATABASE_URL = "sqlite:///./digital_bodyguard.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Every model (table) we create will inherit from this Base
Base = declarative_base()


def get_db():
    """
    Used by FastAPI routes to get a database session, and
    automatically close it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
