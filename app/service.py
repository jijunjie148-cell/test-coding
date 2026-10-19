from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from app.errors import TaskNotFoundError, VersionConflictError
from app.models import Task, TaskPriority, TaskStatus
from app.repository import create_task, delete_task, get_task, list_tasks
from app.schemas import CreateTaskRequest, PageResponse, TaskResponse, UpdateTaskRequest


def _find_task(db: Session, task_id: int) -> Task:
    task = get_task(db, task_id)
    if task is None:
        raise TaskNotFoundError(task_id)
    return task


def create(db: Session, payload: CreateTaskRequest) -> TaskResponse:
    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_at=payload.due_at,
    )
    return TaskResponse.model_validate(create_task(db, task))


def list_page(
    db: Session,
    *,
    status: TaskStatus | None,
    priority: TaskPriority | None,
    page: int,
    size: int,
) -> PageResponse[TaskResponse]:
    items, total = list_tasks(
        db,
        status=status,
        priority=priority,
        page=page,
        size=size,
    )
    total_pages = (total + size - 1) // size
    return PageResponse[TaskResponse](
        items=[TaskResponse.model_validate(item) for item in items],
        page=page,
        size=size,
        total_elements=total,
        total_pages=total_pages,
    )


def get(db: Session, task_id: int) -> TaskResponse:
    return TaskResponse.model_validate(_find_task(db, task_id))


def update(db: Session, task_id: int, payload: UpdateTaskRequest) -> TaskResponse:
    task = _find_task(db, task_id)
    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        if value is not None:
            setattr(task, field, value)
    try:
        db.commit()
        db.refresh(task)
    except StaleDataError as exc:
        db.rollback()
        raise VersionConflictError() from exc
    return TaskResponse.model_validate(task)


def delete(db: Session, task_id: int) -> None:
    delete_task(db, _find_task(db, task_id))
