from app.application.dtos.comment_dto import CreateCommentDTO, UpdateCommentDTO
from app.application.services.unit_of_work import UnitOfWork
from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import CommentRepository
from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.user_repository import UserRepository
from app.shared.exceptions.comment_exceptions import CommentNotFoundException
from app.shared.exceptions.task_exceptions import TaskNotFoundException
from app.shared.exceptions.user_exceptions import UserNotFoundException


class CommentUseCases:
    def __init__(
        self,
        comments: CommentRepository,
        tasks: TaskRepository,
        users: UserRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._comments = comments
        self._tasks = tasks
        self._users = users
        self._unit_of_work = unit_of_work

    def create(self, dto: CreateCommentDTO) -> Comment:
        self._ensure_task_exists(dto.task_id)
        self._ensure_user_exists(dto.author_id)
        comment = self._comments.create(
            Comment(id=None, content=dto.content, task_id=dto.task_id, author_id=dto.author_id)
        )
        self._unit_of_work.commit()
        return comment

    def get(self, comment_id: int) -> Comment:
        comment = self._comments.get_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundException(f"Comment {comment_id} was not found.")
        return comment

    def list_all(self) -> list[Comment]:
        return self._comments.list_all()

    def list_by_task(self, task_id: int) -> list[Comment]:
        self._ensure_task_exists(task_id)
        return self._comments.list_by_task(task_id)

    def update(self, comment_id: int, dto: UpdateCommentDTO) -> Comment:
        current = self.get(comment_id)
        comment = self._comments.update(
            Comment(
                id=comment_id,
                content=dto.content,
                task_id=current.task_id,
                author_id=current.author_id,
            )
        )
        self._unit_of_work.commit()
        return comment

    def delete(self, comment_id: int) -> None:
        self.get(comment_id)
        self._comments.delete(comment_id)
        self._unit_of_work.commit()

    def _ensure_task_exists(self, task_id: int) -> None:
        if self._tasks.get_by_id(task_id) is None:
            raise TaskNotFoundException(f"Task {task_id} was not found.")

    def _ensure_user_exists(self, user_id: int) -> None:
        if self._users.get_by_id(user_id) is None:
            raise UserNotFoundException(f"User {user_id} was not found.")