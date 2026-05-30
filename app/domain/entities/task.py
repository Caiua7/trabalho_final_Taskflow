from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.enums.task_priority import TaskPriority
from app.domain.enums.task_status import TaskStatus


@dataclass(slots=True)
class Task:
    id: str
    title: str
    project_id: str
    creator_id: str
    description: str = ""
    assignee_id: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.title = self.title.strip()
        self.project_id = self.project_id.strip()
        self.creator_id = self.creator_id.strip()
        self.description = self.description.strip()
        self.assignee_id = self.assignee_id.strip() if self.assignee_id else None

        if not self.id:
            raise ValueError("Task id must not be empty.")
        if not self.title:
            raise ValueError("Task title must not be empty.")
        if not self.project_id:
            raise ValueError("Task project id must not be empty.")
        if not self.creator_id:
            raise ValueError("Task creator id must not be empty.")

        if self.status is TaskStatus.DONE and self.completed_at is None:
            self.completed_at = datetime.now(UTC)

    def assign_to(self, user_id: str) -> None:
        sanitized_user_id = user_id.strip()
        if not sanitized_user_id:
            raise ValueError("Assignee id must not be empty.")
        self.assignee_id = sanitized_user_id
        self.touch()

    def unassign(self) -> None:
        self.assignee_id = None
        self.touch()

    def update_details(self, title: str, description: str) -> None:
        sanitized_title = title.strip()
        if not sanitized_title:
            raise ValueError("Task title must not be empty.")
        self.title = sanitized_title
        self.description = description.strip()
        self.touch()

    def change_priority(self, priority: TaskPriority) -> None:
        self.priority = priority
        self.touch()

    def change_status(self, status: TaskStatus) -> None:
        self.status = status
        if status is TaskStatus.DONE:
            self.completed_at = datetime.now(UTC)
        else:
            self.completed_at = None
        self.touch()

    def complete(self) -> None:
        self.change_status(TaskStatus.DONE)

    def reopen(self) -> None:
        self.change_status(TaskStatus.TODO)

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC)
