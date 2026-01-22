"""
Configuration module for AI Chatbot with Cohere integration.
Handles LLM provider selection and configuration.
"""

import os
from typing import Literal, Optional

# LLM Provider types
LLM_PROVIDER = Literal["cohere", "openai", "anthropic"]

class Config:
    """Configuration class for AI Chatbot"""

    # Cohere configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    COHERE_MODEL: str = os.getenv("COHERE_MODEL", "command-r-plus")

    # General AI settings
    DEFAULT_LLM_PROVIDER: LLM_PROVIDER = "cohere"

    # FastAPI settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Todo Chatbot"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_backend.db")

    # Authentication - Use the same config as the main app
    JWT_SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    @classmethod
    def get_llm_provider(cls) -> LLM_PROVIDER:
        """Get the configured LLM provider"""
        provider = os.getenv("LLM_PROVIDER", cls.DEFAULT_LLM_PROVIDER)
        if provider not in ["cohere", "openai", "anthropic"]:
            return cls.DEFAULT_LLM_PROVIDER
        return provider  # type: ignore

    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        # For development, allow placeholder values
        if not cls.COHERE_API_KEY:
            print("WARNING: COHERE_API_KEY is not set. Using development mode.")
        elif cls.COHERE_API_KEY == "your-cohere-api-key-here":
            print("WARNING: Using default placeholder COHERE_API_KEY. Replace with a real key in production.")
        return True

# Global config instance
config = Config()