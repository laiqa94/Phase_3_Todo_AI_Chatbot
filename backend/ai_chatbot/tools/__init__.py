"""
Tools registry for AI Todo Chatbot
"""

from .add_task import AddTaskTool
from .list_tasks import ListTasksTool
from .complete_task import CompleteTaskTool
from .delete_task import DeleteTaskTool
from .update_task import UpdateTaskTool

# Registry of all available tools
TOOLS_REGISTRY = {
    AddTaskTool.name(): AddTaskTool,
    ListTasksTool.name(): ListTasksTool,
    CompleteTaskTool.name(): CompleteTaskTool,
    DeleteTaskTool.name(): DeleteTaskTool,
    UpdateTaskTool.name(): UpdateTaskTool,
}

__all__ = [
    'AddTaskTool',
    'ListTasksTool',
    'CompleteTaskTool',
    'DeleteTaskTool',
    'UpdateTaskTool',
    'TOOLS_REGISTRY'
]