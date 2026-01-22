"""
MCP tool for deleting tasks
Implements the delete_task functionality for the AI agent
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from ..database.repositories import TaskRepository
from sqlmodel import Session


class DeleteTaskInput(BaseModel):
    """Input schema for delete_task tool"""
    user_id: int = Field(..., description="ID of the user who owns the task")
    task_id: int = Field(..., description="ID of the task to delete")


class DeleteTaskTool:
    """MCP Tool for deleting tasks from a user's list"""

    @staticmethod
    def name() -> str:
        return "delete_task"

    @staticmethod
    def description() -> str:
        return "Delete a task from the user's task list"

    @staticmethod
    def parameters() -> Dict[str, Any]:
        return DeleteTaskInput.schema()

    @staticmethod
    def execute(input_data: Dict[str, Any], session: Session) -> Dict[str, Any]:
        """
        Execute the delete_task operation

        Args:
            input_data: Dictionary containing user_id and task_id
            session: Database session

        Returns:
            Dictionary with result of the operation
        """
        try:
            # Validate input
            params = DeleteTaskInput(**input_data)

            # Create task repository
            task_repo = TaskRepository(session)

            # Delete the task
            success = task_repo.delete_task(task_id=params.task_id, user_id=params.user_id)

            if success:
                return {
                    "success": True,
                    "task_id": params.task_id,
                    "message": f"Task with ID {params.task_id} has been deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Task with ID {params.task_id} not found or you don't have permission to delete it"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete task. Please check your input and try again."
            }