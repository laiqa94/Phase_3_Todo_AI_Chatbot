"""
Database engine and session setup for AI Todo Chatbot
"""

from sqlmodel import create_engine, Session
from .models import SQLModel
from ..config import config
from sqlalchemy.exc import OperationalError

# Create database engine
engine = create_engine(
    config.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True
)


def create_db_and_tables():
    """Create database tables"""
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Database initialization warning: {e}")
        print("Continuing with existing database...")


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session