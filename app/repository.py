from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Task, TaskPriority, TaskStatus


def create_task(db: Session, task: Task) -> Task:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def list_tasks(
    db: Session,
    *,
    status: TaskStatus | None,
    priority: TaskPriority | None,
    page: int,
    size: int,
) -> tuple[list[Task], int]:
    filters = []
    if status is not None:
        filters.append(Task.status == status)
    if priority is not None:
        filters.append(Task.priority == priority)

    total = db.scalar(select(func.count()).select_from(Task).where(*filters)) or 0
    statement = (
        select(Task)
        .where(*filters)
        .order_by(Task.created_at.desc(), Task.id.desc())
        .offset(page * size)
        .limit(size)
    )
    return list(db.scalars(statement).all()), int(total)


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
