"""
Cohere AI Provider for AI Todo Chatbot
Handles communication with Cohere API
"""

import cohere
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ..config import config


class CohereProvider:
    """Provider class for Cohere API integration"""

    def __init__(self):
        if not config.COHERE_API_KEY or config.COHERE_API_KEY == "your-cohere-api-key-here":
            # In development mode, set client to None to indicate we're using mock mode
            self.client = None
        else:
            self.client = cohere.Client(config.COHERE_API_KEY)

        self.model = config.COHERE_MODEL

    def chat(self,
             messages: List[Dict[str, str]],
             tools: Optional[List[Dict[str, Any]]] = None,
             temperature: float = 0.7) -> Dict[str, Any]:
        """
        Send chat request to Cohere API

        Args:
            messages: List of message dictionaries with 'role' and 'message' keys
            tools: Optional list of tool definitions
            temperature: Temperature for response creativity

        Returns:
            Response dictionary from Cohere API
        """
        # Check if we're in development mode with mock API key
        if not config.COHERE_API_KEY or config.COHERE_API_KEY == "your-cohere-api-key-here" or config.COHERE_API_KEY == "":
            # Return enhanced mock response for development
            user_message = messages[-1]["content"].strip().lower()
            original_message = messages[-1]["content"]

            # Enhanced rule-based responses for development
            if any(greeting in user_message for greeting in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
                response_text = "Hello! 👋 I'm your AI assistant. How can I help you with your tasks today?"
            elif any(word in user_message for word in ["help", "what can you do", "assist"]):
                response_text = "I can help you manage your tasks! You can ask me to add, list, update, or complete tasks. For example: 'Add a task to buy groceries' or 'Show me my tasks'."
            elif any(action in user_message for action in ["add", "create", "make"]) and any(word in user_message for word in ["task", "todo"]):
                response_text = "Sure! I can help you add a task. What would you like to name your task?"
            elif any(word in user_message for word in ["list", "show", "display", "my tasks", "all tasks"]):
                response_text = "Here are your tasks: [Sample Task 1, Sample Task 2]. Would you like to modify any of these or add a new task?"
            elif any(word in user_message for word in ["complete", "done", "finish", "mark as done"]):
                response_text = "I've marked that task as complete! 🎉 Is there anything else you'd like to do?"
            elif any(word in user_message for word in ["update", "change", "modify", "edit"]):
                response_text = "I can help you update your tasks. What changes would you like to make?"
            elif any(word in user_message for word in ["delete", "remove", "cancel"]):
                response_text = "I can help you remove tasks. Which task would you like to delete?"
            elif len(user_message) == 0 or user_message.isspace():
                response_text = "Hi there! Please type a message so I can help you with your tasks."
            elif len(user_message.split()) == 1:
                # Single word input, respond with a question
                response_text = f"You said '{original_message}'. How can I help you with your tasks?"
            else:
                # For any other input, provide a helpful response
                response_text = f"I received your message: '{original_message}'. I'm here to help you manage your tasks. You can ask me to add, list, update, or complete tasks."

            # Ensure we always return a non-empty response
            if not response_text or response_text.strip() == "":
                response_text = "I'm your AI assistant for task management. How can I help you today?"

            return {
                "text": response_text,
                "finish_reason": "COMPLETE",
                "tool_calls": [],  # No tool calls in mock mode
                "meta": {"development_mode": True}
            }

        # Convert messages to Cohere format
        chat_history = []
        for msg in messages:
            role = "USER" if msg["role"] == "user" else "CHATBOT"
            chat_history.append({
                "user_name": role,
                "text": msg["content"]
            })

        # Prepare the request
        kwargs = {
            "message": messages[-1]["content"],  # Last message is the current prompt
            "chat_history": chat_history[:-1],  # All previous messages as history
            "model": self.model,
            "temperature": temperature,
        }

        # Add tools if provided
        if tools:
            kwargs["tools"] = tools

        try:
            response = self.client.chat(**kwargs)
            return {
                "text": response.text,
                "finish_reason": getattr(response, 'finish_reason', 'COMPLETE'),
                "tool_calls": getattr(response, 'tool_calls', []),
                "meta": getattr(response, 'meta', {})
            }
        except Exception as e:
            return {
                "error": str(e),
                "text": "Sorry, I encountered an error processing your request. Please try again.",
                "finish_reason": "ERROR"
            }

    def generate(self,
                 prompt: str,
                 max_tokens: int = 300,
                 temperature: float = 0.7) -> str:
        """
        Generate text using Cohere's generate endpoint

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Temperature for response creativity

        Returns:
            Generated text
        """
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.generations[0].text if response.generations else ""
        except Exception as e:
            return f"Error generating response: {str(e)}"