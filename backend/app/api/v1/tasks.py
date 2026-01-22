from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.core.db import get_session
from app.models.task import Task, TaskCreate, TaskUpdate
from app.models.user import User
from app.schemas.task import TaskRead, TaskCreate as TaskCreateSchema, TaskUpdate as TaskUpdateSchema
from app.services.task import (
    create_task, get_tasks_by_owner, get_task_by_id,
    update_task, delete_task, toggle_task_completion, get_tasks_by_status
)
from .deps import get_current_user


tasks_router = APIRouter()


@tasks_router.post("/", response_model=TaskRead)
def create_new_task(
    task: TaskCreateSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return create_task(session=session, task_create=task, owner_id=current_user.id)


@tasks_router.get("", response_model=List[TaskRead])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: bool = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if completed is not None:
        tasks = get_tasks_by_status(session=session, owner_id=current_user.id, completed=completed, skip=skip, limit=limit)
    else:
        tasks = get_tasks_by_owner(session=session, owner_id=current_user.id, skip=skip, limit=limit)
    return tasks


@tasks_router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(session=session, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.put("/{task_id}", response_model=TaskRead)
def update_existing_task(
    task_id: int,
    task_update: TaskUpdateSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(session=session, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return update_task(session=session, db_task=task, task_update=task_update)


@tasks_router.delete("/{task_id}")
def delete_existing_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(session=session, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_task(session=session, db_task=task)
    return {"message": "Task deleted successfully"}


@tasks_router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task_completion_status(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(session=session, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return toggle_task_completion(session=session, db_task=task)