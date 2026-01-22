#!/usr/bin/env python
"""
Simple script to create the database and a test user
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.security import get_password_hash

def create_database_and_test_user():
    print("Creating database and test user...")

    # Use the same database file as configured
    db_path = "todo_backend.db"

    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the users table (matching the User model structure)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            full_name TEXT,
            hashed_password TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )
    ''')

    # Commit the table creation
    conn.commit()

    # Check if test user already exists
    cursor.execute("SELECT id FROM user WHERE email = ?", ("test@example.com",))
    result = cursor.fetchone()

    if result:
        print(f"Test user already exists with ID: {result[0]}")
    else:
        # Create a test user
        hashed_password = get_password_hash("password123")
        cursor.execute('''
            INSERT INTO user (email, full_name, hashed_password, created_at)
            VALUES (?, ?, ?, ?)
        ''', ("test@example.com", "Test User", hashed_password, datetime.utcnow()))

        conn.commit()
        user_id = cursor.lastrowid
        print(f"Created test user with ID: {user_id}")

    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    create_database_and_test_user()