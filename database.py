"""
Database configuration via SQLAlchemy.

Uses PostgreSQL when DATABASE_URL is set (production), otherwise SQLite (local dev).
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Production: PostgreSQL (Railway, etc.)
    engine = create_engine(DATABASE_URL)
else:
    # Local dev: SQLite
    engine = create_engine(
        "sqlite:///./surveys.db",
        connect_args={"check_same_thread": False},  # Required for SQLite
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a SQLAlchemy session and ensures cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
