"""
Server startup script for AI Todo Chatbot
"""

from .main import app
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "false").lower() == "true"

    print(f"Starting AI Todo Chatbot server on {host}:{port}")
    print(f"Reload mode: {reload}")

    uvicorn.run(
        "backend.ai_chatbot.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )