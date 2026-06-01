from app.domain.entities.task import Task
from app.domain.enums.task_priority import TaskPriority
from app.domain.enums.task_status import TaskStatus


class TaskFactory:
    def create(
        self,
        title: str,
        description: str,
        priority: TaskPriority,
        project_id: int,
        assignee_id: int | None = None,
    ) -> Task:
        return Task(
            id=None,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            priority=priority,
            assignee_id=assignee_id,
            project_id=project_id,
        )