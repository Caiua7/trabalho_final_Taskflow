from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus


@dataclass(frozen=True, slots=True)
class TaskStatusChangedEvent:
    task: Task
    previous_status: TaskStatus
    new_status: TaskStatus


class Observer(ABC):
    @abstractmethod
    def update(self, event: TaskStatusChangedEvent) -> None:
        raise NotImplementedError


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        raise NotImplementedError

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        raise NotImplementedError

    @abstractmethod
    def notify(self, event: TaskStatusChangedEvent) -> None:
        raise NotImplementedError


class TaskStatusSubject(Subject):
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: TaskStatusChangedEvent) -> None:
        for observer in self._observers:
            observer.update(event)