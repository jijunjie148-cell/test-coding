from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import TaskPriority, TaskStatus
from app.schemas import CreateTaskRequest, PageResponse, TaskResponse, UpdateTaskRequest
from app.service import create, delete, get, list_page, update


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    payload: CreateTaskRequest,
    db: Session = Depends(get_db),
) -> TaskResponse:
    return create(db, payload)


@router.get("", response_model=PageResponse[TaskResponse])
def list_tasks_endpoint(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = Query(default=None),
    page: int = Query(default=0, ge=0),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PageResponse[TaskResponse]:
    return list_page(
        db,
        status=status_filter,
        priority=priority,
        page=page,
        size=size,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    return get(db, task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    payload: UpdateTaskRequest,
    db: Session = Depends(get_db),
) -> TaskResponse:
    return update(db, task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)) -> Response:
    delete(db, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
