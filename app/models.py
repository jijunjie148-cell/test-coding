from datetime import datetime
from enum import Enum
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, Enum as SqlEnum, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


APP_ZONE = ZoneInfo("Asia/Shanghai")


def now_local() -> datetime:
    return datetime.now(APP_ZONE).replace(tzinfo=None)


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_tasks_status_due_at", "status", "due_at"),
        Index("idx_tasks_priority_created_at", "priority", "created_at"),
        Index("idx_tasks_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus, native_enum=False, length=20),
        nullable=False,
        default=TaskStatus.TODO,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SqlEnum(TaskPriority, native_enum=False, length=20),
        nullable=False,
        default=TaskPriority.MEDIUM,
    )
    due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=now_local
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=now_local, onupdate=now_local
    )

    __mapper_args__ = {"version_id_col": version}
