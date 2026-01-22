#!/usr/bin/env python3
"""
Script to create a test user for development
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlmodel import Session, select
from app.core.db import engine
from app.models.user import User
from app.core.security import get_password_hash

def create_test_user():
    """Create a test user for development"""
    with Session(engine) as session:
        # Check if test user already exists
        statement = select(User).where(User.email == "test@example.com")
        existing_user = session.exec(statement).first()
        
        if existing_user:
            print(f"Test user already exists with ID: {existing_user.id}")
            return existing_user.id
        
        # Create test user
        test_user = User(
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("testpassword123")
        )
        
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        
        print(f"Created test user with ID: {test_user.id}")
        return test_user.id

if __name__ == "__main__":
    user_id = create_test_user()
    print(f"Test user ready with ID: {user_id}")