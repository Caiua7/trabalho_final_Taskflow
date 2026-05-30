from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    def add(self, comment: Comment) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, comment_id: str) -> Comment | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_task(self, task_id: str) -> list[Comment]:
        raise NotImplementedError

    @abstractmethod
    def update(self, comment: Comment) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def remove(self, comment_id: str) -> None:
        raise NotImplementedError
