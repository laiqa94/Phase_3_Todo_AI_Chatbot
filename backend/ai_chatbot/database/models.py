"""
Database models for AI Todo Chatbot using SQLModel
Defines Task, Conversation, and Message entities with proper relationships
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

if TYPE_CHECKING:
    from .models import Task


# User model - Use the same model as the main application
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app.models.user import User


# Task model
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)
    priority: Optional[str] = Field(default="medium", max_length=20)  # low, medium, high
    user_id: int = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    __tablename__ = "ai_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship()


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None  # low, medium, high


# Conversation model
class ConversationBase(SQLModel):
    title: Optional[str] = Field(default="New Conversation", max_length=255)
    user_id: int = Field(foreign_key="user.id")


class Conversation(ConversationBase, table=True):
    __tablename__ = "ai_conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship()
    messages: list["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime


# Message model
class MessageBase(SQLModel):
    role: str = Field(max_length=20)  # user, assistant, system
    content: str = Field(min_length=1)
    conversation_id: int = Field(foreign_key="ai_conversations.id")


class Message(MessageBase, table=True):
    __tablename__ = "ai_messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Conversation = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    created_at: datetime


# Link User to related models
User.model_rebuild()

Conversation.model_rebuild()
