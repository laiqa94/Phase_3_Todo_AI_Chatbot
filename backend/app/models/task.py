from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    if TYPE_CHECKING:
        user: "User" = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# Ensure relationships are properly configured
try:
    Task.model_rebuild()
except AttributeError:
    # Handle case where model_rebuild is not available
    pass