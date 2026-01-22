"""
MCP tool for completing tasks
Implements the complete_task functionality for the AI agent
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from ..database.repositories import TaskRepository
from sqlmodel import Session


class CompleteTaskInput(BaseModel):
    """Input schema for complete_task tool"""
    user_id: int = Field(..., description="ID of the user who owns the task")
    task_id: int = Field(..., description="ID of the task to complete/incomplete")
    completed: bool = Field(default=True, description="Whether to mark task as completed (True) or pending (False)")


class CompleteTaskTool:
    """MCP Tool for marking tasks as completed or pending"""

    @staticmethod
    def name() -> str:
        return "complete_task"

    @staticmethod
    def description() -> str:
        return "Mark a task as completed or pending"

    @staticmethod
    def parameters() -> Dict[str, Any]:
        return CompleteTaskInput.schema()

    @staticmethod
    def execute(input_data: Dict[str, Any], session: Session) -> Dict[str, Any]:
        """
        Execute the complete_task operation

        Args:
            input_data: Dictionary containing user_id, task_id, and completed status
            session: Database session

        Returns:
            Dictionary with result of the operation
        """
        try:
            # Validate input
            params = CompleteTaskInput(**input_data)

            # Create task repository
            task_repo = TaskRepository(session)

            # Update task completion status
            task = task_repo.complete_task(
                task_id=params.task_id,
                user_id=params.user_id,
                completed=params.completed
            )

            if task:
                status_text = "completed" if params.completed else "pending"
                return {
                    "success": True,
                    "task_id": task.id,
                    "title": task.title,
                    "completed": task.completed,
                    "message": f"Task '{task.title}' has been marked as {status_text}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Task with ID {params.task_id} not found or you don't have permission to modify it"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task completion status. Please check your input and try again."
            }