from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.project import Project


class ProjectRepository(ABC):
    @abstractmethod
    def add(self, project: Project) -> Project:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, project_id: str) -> Project | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Project]:
        raise NotImplementedError

    @abstractmethod
    def list_by_owner(self, owner_id: str) -> list[Project]:
        raise NotImplementedError

    @abstractmethod
    def update(self, project: Project) -> Project:
        raise NotImplementedError

    @abstractmethod
    def remove(self, project_id: str) -> None:
        raise NotImplementedError
