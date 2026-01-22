#!/usr/bin/env python
"""
Initialize the database with required tables and a test user
"""

import os
import sys

# Add the backend directory to Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel, create_engine, Session, select
from app.models.user import User
from ai_chatbot.database.engine import create_db_and_tables
from app.core.security import get_password_hash

def initialize_database():
    print("Initializing database...")

    # Create database and tables
    create_db_and_tables()

    # Use the same database as configured
    from ai_chatbot.config import config
    engine = create_engine(config.DATABASE_URL)

    with Session(engine) as session:
        # Check if test user already exists
        existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()

        if not existing_user:
            # Create a test user
            test_user = User(
                email="test@example.com",
                full_name="Test User",
                hashed_password=get_password_hash("password123")
            )

            session.add(test_user)
            session.commit()
            session.refresh(test_user)

            print(f"Created test user with ID: {test_user.id}")
        else:
            print(f"Test user already exists with ID: {existing_user.id}")

    print("Database initialization complete!")

if __name__ == "__main__":
    initialize_database()