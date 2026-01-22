"""
Simplified main application for the Todo Application with AI Chatbot
This version avoids complex module imports that cause issues
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the main application
app = FastAPI(title="Todo Application with AI Chatbot", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, configure specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to include the AI chatbot routes
try:
    from backend.ai_chatbot.api.chat_endpoint import router as chat_router
    app.include_router(chat_router, prefix="/api/v1", tags=["chatbot"])
    print("AI Chatbot routes loaded successfully")
except ImportError as e:
    print(f"Warning: Could not load AI chatbot routes: {e}")
    # Try alternative import
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__)))
        from ai_chatbot.api.chat_endpoint import router as chat_router
        app.include_router(chat_router, prefix="/api/v1", tags=["chatbot"])
        print("AI Chatbot routes loaded successfully via alternative import")
    except ImportError as e2:
        print(f"Warning: Alternative import also failed: {e2}")

# Simple root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Todo Application with AI Chatbot",
        "version": "1.0.0",
        "services": [
            "GET /health - Health check",
            "POST /api/v1/{user_id}/chat - Chat with AI assistant",
            "POST /api/v1/{user_id}/new_conversation - Start new conversation"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Todo Application with AI Chatbot"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)