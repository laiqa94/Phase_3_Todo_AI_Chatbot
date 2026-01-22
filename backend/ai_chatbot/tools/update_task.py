"""
MCP tool for updating tasks
Implements the update_task functionality for the AI agent
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..database.repositories import TaskRepository
from ..database.models import TaskUpdate
from sqlmodel import Session


class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool"""
    user_id: int = Field(..., description="ID of the user who owns the task")
    task_id: int = Field(..., description="ID of the task to update")
    title: Optional[str] = Field(None, description="New title for the task")
    description: Optional[str] = Field(None, description="New description for the task")
    priority: Optional[str] = Field(None, description="New priority for the task (low, medium, high)")
    due_date: Optional[str] = Field(None, description="New due date in ISO format (YYYY-MM-DD)")


class UpdateTaskTool:
    """MCP Tool for updating task properties"""

    @staticmethod
    def name() -> str:
        return "update_task"

    @staticmethod
    def description() -> str:
        return "Update properties of an existing task"

    @staticmethod
    def parameters() -> Dict[str, Any]:
        return UpdateTaskInput.schema()

    @staticmethod
    def execute(input_data: Dict[str, Any], session: Session) -> Dict[str, Any]:
        """
        Execute the update_task operation

        Args:
            input_data: Dictionary containing user_id, task_id, and fields to update
            session: Database session

        Returns:
            Dictionary with result of the operation
        """
        try:
            # Validate input
            params = UpdateTaskInput(**input_data)

            # Create task repository
            task_repo = TaskRepository(session)

            # Prepare update data
            update_data = {}
            if params.title is not None:
                update_data['title'] = params.title
            if params.description is not None:
                update_data['description'] = params.description
            if params.priority is not None:
                update_data['priority'] = params.priority
            if params.due_date is not None:
                from datetime import datetime
                update_data['due_date'] = datetime.fromisoformat(params.due_date.replace('Z', '+00:00'))

            # Check if there's anything to update
            if not update_data:
                return {
                    "success": False,
                    "message": "No fields provided to update"
                }

            # Create TaskUpdate object
            task_update = TaskUpdate(**{k: v for k, v in update_data.items() if v is not None})

            # Update the task
            updated_task = task_repo.update_task(
                task_id=params.task_id,
                task_update=task_update,
                user_id=params.user_id
            )

            if updated_task:
                return {
                    "success": True,
                    "task_id": updated_task.id,
                    "title": updated_task.title,
                    "updated_fields": list(update_data.keys()),
                    "message": f"Task '{updated_task.title}' has been updated successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Task with ID {params.task_id} not found or you don't have permission to update it"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task. Please check your input and try again."
            }