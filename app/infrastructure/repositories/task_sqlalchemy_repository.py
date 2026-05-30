from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.task import Task
from app.domain.enums.task_priority import TaskPriority
from app.domain.enums.task_status import TaskStatus
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.database.models import TaskModel


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, task: Task) -> Task:
        model = TaskModel(
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            assignee_id=task.assignee_id,
            project_id=task.project_id,
        )
        self._session.add(model)
        self._session.flush()
        return self._to_entity(model)

    def get_by_id(self, task_id: int) -> Task | None:
        model = self._session.get(TaskModel, task_id)
        return self._to_entity(model) if model else None

    def list_all(self) -> list[Task]:
        models = self._session.scalars(select(TaskModel).order_by(TaskModel.id)).all()
        return [self._to_entity(model) for model in models]

    def list_by_project(self, project_id: int) -> list[Task]:
        statement = select(TaskModel).where(TaskModel.project_id == project_id).order_by(TaskModel.id)
        models = self._session.scalars(statement).all()
        return [self._to_entity(model) for model in models]

    def list_by_status(self, status: TaskStatus) -> list[Task]:
        statement = select(TaskModel).where(TaskModel.status == status.value).order_by(TaskModel.id)
        models = self._session.scalars(statement).all()
        return [self._to_entity(model) for model in models]

    def update(self, task: Task) -> Task:
        model = self._session.get(TaskModel, task.id)
        if model is None:
            raise ValueError("Cannot update a missing task.")
        model.title = task.title
        model.description = task.description
        model.status = task.status.value
        model.priority = task.priority.value
        model.assignee_id = task.assignee_id
        model.project_id = task.project_id
        self._session.flush()
        return self._to_entity(model)

    def delete(self, task_id: int) -> None:
        model = self._session.get(TaskModel, task_id)
        if model is not None:
            self._session.delete(model)
            self._session.flush()

    @staticmethod
    def _to_entity(model: TaskModel) -> Task:
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            status=TaskStatus(model.status),
            priority=TaskPriority(model.priority),
            assignee_id=model.assignee_id,
            project_id=model.project_id,
        )