from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None


class User(UserBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    if TYPE_CHECKING:
        # Relationship for tasks (works with both main app and ai_chatbot Task models)
        # This needs to be compatible with the ai_chatbot Task model's relationship
        tasks: list["Task"] = []
        # Relationship for ai_chatbot conversations
        conversations: list["Conversation"] = []


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime


# Ensure relationships are properly configured
try:
    User.model_rebuild()
except AttributeError:
    # Handle case where model_rebuild is not available
    pass