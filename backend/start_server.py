#!/usr/bin/env python
"""
Simple script to start the backend server without complex dependency resolution
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Change to the project root directory
os.chdir(project_root)

if __name__ == "__main__":
    # Import the main app directly from the project structure
    from main import app

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"Starting server on {host}:{port}")
    print("Press Ctrl+C to stop the server")

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False  # Disable reload for cleaner output
    )