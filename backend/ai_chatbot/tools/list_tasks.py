"""
MCP tool for listing tasks
Implements the list_tasks functionality for the AI agent
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from ..database.repositories import TaskRepository
from sqlmodel import Session


class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool"""
    user_id: int = Field(..., description="ID of the user whose tasks to list")
    status: str = Field(default="all", description="Status filter: 'all', 'pending', or 'completed'")


class ListTasksTool:
    """MCP Tool for listing tasks from a user's list"""

    @staticmethod
    def name() -> str:
        return "list_tasks"

    @staticmethod
    def description() -> str:
        return "List tasks from the user's task list with optional filtering"

    @staticmethod
    def parameters() -> Dict[str, Any]:
        return ListTasksInput.schema()

    @staticmethod
    def execute(input_data: Dict[str, Any], session: Session) -> Dict[str, Any]:
        """
        Execute the list_tasks operation

        Args:
            input_data: Dictionary containing user_id and status filter
            session: Database session

        Returns:
            Dictionary with list of tasks
        """
        try:
            # Validate input
            params = ListTasksInput(**input_data)

            # Validate status parameter
            valid_statuses = ["all", "pending", "completed"]
            if params.status not in valid_statuses:
                params.status = "all"

            # Create task repository
            task_repo = TaskRepository(session)

            # Get tasks based on status filter
            tasks = task_repo.get_tasks_by_user(
                user_id=params.user_id,
                status=params.status if params.status != "all" else None
            )

            # Format tasks for response
            task_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                if task.description:
                    task_dict["description"] = task.description
                if task.due_date:
                    task_dict["due_date"] = task.due_date.isoformat()

                task_list.append(task_dict)

            status_desc = params.status if params.status != "all" else "all"
            return {
                "success": True,
                "task_count": len(task_list),
                "status_filter": params.status,
                "tasks": task_list,
                "message": f"Found {len(task_list)} {status_desc} tasks"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to list tasks. Please try again."
            }