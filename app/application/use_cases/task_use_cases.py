from app.application.dtos.task_dto import AssignTaskDTO, ChangeTaskStatusDTO, CreateTaskDTO, UpdateTaskDTO
from app.application.services.status_strategies import StatusStrategyResolver
from app.application.services.unit_of_work import UnitOfWork
from app.domain.entities.task import Task
from app.domain.enums.task_status import TaskStatus
from app.domain.repositories.project_repository import ProjectRepository
from app.domain.repositories.task_repository import TaskRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.observer import Subject, TaskStatusChangedEvent
from app.domain.services.task_factory import TaskFactory
from app.shared.exceptions.project_exceptions import ProjectNotFoundException
from app.shared.exceptions.task_exceptions import TaskNotFoundException
from app.shared.exceptions.user_exceptions import UserNotFoundException


class TaskUseCases:
    def __init__(
        self,
        tasks: TaskRepository,
        users: UserRepository,
        projects: ProjectRepository,
        unit_of_work: UnitOfWork,
        task_factory: TaskFactory,
        status_strategy_resolver: StatusStrategyResolver,
        status_subject: Subject,
    ) -> None:
        self._tasks = tasks
        self._users = users
        self._projects = projects
        self._unit_of_work = unit_of_work
        self._task_factory = task_factory
        self._status_strategy_resolver = status_strategy_resolver
        self._status_subject = status_subject

    def create(self, dto: CreateTaskDTO) -> Task:
        self._ensure_project_exists(dto.project_id)
        if dto.assignee_id is not None:
            self._ensure_user_exists(dto.assignee_id)

        task = self._task_factory.create(
            title=dto.title,
            description=dto.description,
            priority=dto.priority,
            project_id=dto.project_id,
            assignee_id=dto.assignee_id,
        )
        task = self._tasks.create(task)
        self._unit_of_work.commit()
        return task

    def get(self, task_id: int) -> Task:
        task = self._tasks.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundException(f"Task {task_id} was not found.")
        return task

    def list_all(self) -> list[Task]:
        return self._tasks.list_all()

    def list_by_project(self, project_id: int) -> list[Task]:
        self._ensure_project_exists(project_id)
        return self._tasks.list_by_project(project_id)

    def list_by_status(self, status: TaskStatus) -> list[Task]:
        return self._tasks.list_by_status(status)

    def update(self, task_id: int, dto: UpdateTaskDTO) -> Task:
        self.get(task_id)
        self._ensure_project_exists(dto.project_id)
        if dto.assignee_id is not None:
            self._ensure_user_exists(dto.assignee_id)

        task = self._tasks.update(
            Task(
                id=task_id,
                title=dto.title,
                description=dto.description,
                status=self.get(task_id).status,
                priority=dto.priority,
                assignee_id=dto.assignee_id,
                project_id=dto.project_id,
            )
        )
        self._unit_of_work.commit()
        return task

    def assign(self, task_id: int, dto: AssignTaskDTO) -> Task:
        task = self.get(task_id)
        self._ensure_user_exists(dto.assignee_id)
        task.assign_to(dto.assignee_id)
        task = self._tasks.update(task)
        self._unit_of_work.commit()
        return task

    def change_status(self, task_id: int, dto: ChangeTaskStatusDTO) -> Task:
        task = self.get(task_id)
        previous_status = task.status
        strategy = self._status_strategy_resolver.resolve(previous_status, dto.status)
        strategy.apply(task, dto.status)
        task = self._tasks.update(task)
        self._unit_of_work.commit()

        if previous_status != task.status:
            self._status_subject.notify(
                TaskStatusChangedEvent(
                    task=task,
                    previous_status=previous_status,
                    new_status=task.status,
                )
            )
        return task

    def delete(self, task_id: int) -> None:
        self.get(task_id)
        self._tasks.delete(task_id)
        self._unit_of_work.commit()

    def _ensure_user_exists(self, user_id: int) -> None:
        if self._users.get_by_id(user_id) is None:
            raise UserNotFoundException(f"User {user_id} was not found.")

    def _ensure_project_exists(self, project_id: int) -> None:
        if self._projects.get_by_id(project_id) is None:
            raise ProjectNotFoundException(f"Project {project_id} was not found.")