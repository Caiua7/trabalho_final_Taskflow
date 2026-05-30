from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, user: User) -> User:
        model = UserModel(name=user.name, email=user.email)
        self._session.add(model)
        self._session.flush()
        return self._to_entity(model)

    def get_by_id(self, user_id: int) -> User | None:
        model = self._session.get(UserModel, user_id)
        return self._to_entity(model) if model else None

    def list_all(self) -> list[User]:
        models = self._session.scalars(select(UserModel).order_by(UserModel.id)).all()
        return [self._to_entity(model) for model in models]

    def update(self, user: User) -> User:
        model = self._session.get(UserModel, user.id)
        if model is None:
            raise ValueError("Cannot update a missing user.")
        model.name = user.name
        model.email = user.email
        self._session.flush()
        return self._to_entity(model)

    def delete(self, user_id: int) -> None:
        model = self._session.get(UserModel, user_id)
        if model is not None:
            self._session.delete(model)
            self._session.flush()

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(id=model.id, name=model.name, email=model.email)