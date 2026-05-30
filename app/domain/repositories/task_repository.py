from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_project(self, project_id: str) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def list_by_assignee(self, assignee_id: str) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def list_by_status(self, status: TaskStatus) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def update(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def remove(self, task_id: str) -> None:
        raise NotImplementedError
