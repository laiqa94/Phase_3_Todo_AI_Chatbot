"""
Main FastAPI application for the Todo Application with AI Chatbot
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main app that contains both todo and chatbot functionality
from app.main import app  # This app includes both todo and chatbot routes

# The app is already configured in app.main, so we don't need to add middleware again
# The routes are already included in app.main

# The routes are already defined in app.main, so no need to redefine them here
# The app instance already includes all necessary routes and middleware

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)