from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import CommentRepository
from app.infrastructure.database.models import CommentModel


class SqlAlchemyCommentRepository(CommentRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, comment: Comment) -> Comment:
        model = CommentModel(
            content=comment.content,
            task_id=comment.task_id,
            author_id=comment.author_id,
        )
        self._session.add(model)
        self._session.flush()
        return self._to_entity(model)

    def get_by_id(self, comment_id: int) -> Comment | None:
        model = self._session.get(CommentModel, comment_id)
        return self._to_entity(model) if model else None

    def list_all(self) -> list[Comment]:
        models = self._session.scalars(select(CommentModel).order_by(CommentModel.id)).all()
        return [self._to_entity(model) for model in models]

    def list_by_task(self, task_id: int) -> list[Comment]:
        statement = select(CommentModel).where(CommentModel.task_id == task_id).order_by(CommentModel.id)
        models = self._session.scalars(statement).all()
        return [self._to_entity(model) for model in models]

    def update(self, comment: Comment) -> Comment:
        model = self._session.get(CommentModel, comment.id)
        if model is None:
            raise ValueError("Cannot update a missing comment.")
        model.content = comment.content
        self._session.flush()
        return self._to_entity(model)

    def delete(self, comment_id: int) -> None:
        model = self._session.get(CommentModel, comment_id)
        if model is not None:
            self._session.delete(model)
            self._session.flush()

    @staticmethod
    def _to_entity(model: CommentModel) -> Comment:
        return Comment(
            id=model.id,
            content=model.content,
            task_id=model.task_id,
            author_id=model.author_id,
        )