from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.project import Project
from app.domain.repositories.project_repository import ProjectRepository
from app.infrastructure.database.models import ProjectModel


class SqlAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, project: Project) -> Project:
        model = ProjectModel(name=project.name, description=project.description)
        self._session.add(model)
        self._session.flush()
        return self._to_entity(model)

    def get_by_id(self, project_id: int) -> Project | None:
        model = self._session.get(ProjectModel, project_id)
        return self._to_entity(model) if model else None

    def list_all(self) -> list[Project]:
        models = self._session.scalars(select(ProjectModel).order_by(ProjectModel.id)).all()
        return [self._to_entity(model) for model in models]

    def update(self, project: Project) -> Project:
        model = self._session.get(ProjectModel, project.id)
        if model is None:
            raise ValueError("Cannot update a missing project.")
        model.name = project.name
        model.description = project.description
        self._session.flush()
        return self._to_entity(model)

    def delete(self, project_id: int) -> None:
        model = self._session.get(ProjectModel, project_id)
        if model is not None:
            self._session.delete(model)
            self._session.flush()

    @staticmethod
    def _to_entity(model: ProjectModel) -> Project:
        return Project(id=model.id, name=model.name, description=model.description)