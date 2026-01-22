#!/usr/bin/env python
"""
Script to run the backend server with AI Chatbot
"""

import sys
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the workspace directory to Python path to resolve backend modules
project_root = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(project_root)
sys.path.insert(0, workspace_root)

def run_server():
    print("Starting Todo Backend with AI Chatbot...")
    print("Loading configuration...")

    try:
        # Import the main app that includes AI chatbot routes
        from backend.app.main import app
        print("App imported successfully")

        # Get port from environment or default to 8001 to avoid conflicts
        port = int(os.environ.get("PORT", 8001))
        host = os.environ.get("HOST", "0.0.0.0")

        print(f"Server will start on {host}:{port}")
        print("Available endpoints:")
        print("- Regular Todo API: /api/v1/")
        print("- AI Chatbot: /api/v1/{user_id}/chat")
        print("- Health check: /")
        print("\nPress Ctrl+C to stop the server\n")

        # Run the server
        uvicorn.run(
            "backend.app.main:app",
            host=host,
            port=port,
            reload=False,  # Enable auto-reload during development
            log_level="info"
        )

    except ImportError as e:
        print(f"Error importing application: {e}")
        print("Make sure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_server()