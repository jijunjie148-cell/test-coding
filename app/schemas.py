from datetime import datetime
from typing import Generic, TypeVar
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import TaskPriority, TaskStatus, now_local


APP_ZONE = ZoneInfo("Asia/Shanghai")
T = TypeVar("T")


def _local_naive(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(APP_ZONE).replace(tzinfo=None)


class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=4000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must not be blank")
        return value.strip()

    @field_validator("due_at")
    @classmethod
    def due_at_must_be_future(cls, value: datetime | None) -> datetime | None:
        if value is not None and _local_naive(value) <= now_local():
            raise ValueError("due_at must be in the future")
        return value


class UpdateTaskRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=4000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("title must not be blank")
        return value.strip() if value is not None else None

    @field_validator("due_at")
    @classmethod
    def due_at_must_be_future(cls, value: datetime | None) -> datetime | None:
        if value is not None and _local_naive(value) <= now_local():
            raise ValueError("due_at must be in the future")
        return value


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_at: datetime | None
    version: int
    created_at: datetime
    updated_at: datetime


class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    size: int
    total_elements: int
    total_pages: int
