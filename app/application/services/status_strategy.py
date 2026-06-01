from abc import ABC, abstractmethod

from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus


class StatusStrategy(ABC):
    @abstractmethod
    def can_apply(self, current_status: TaskStatus, new_status: TaskStatus) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, task: Task, new_status: TaskStatus) -> None:
        raise NotImplementedError