from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.services.observer import Observer, TaskStatusChangedEvent


@dataclass(frozen=True, slots=True)
class Notification:
    task_id: int | None
    message: str
    created_at: datetime


class NotificationObserver(Observer):
    def __init__(self) -> None:
        self._notifications: list[Notification] = []

    def update(self, event: TaskStatusChangedEvent) -> None:
        self._notifications.append(
            Notification(
                task_id=event.task.id,
                message=(
                    f"Task {event.task.id} changed from "
                    f"{event.previous_status.value} to {event.new_status.value}."
                ),
                created_at=datetime.now(UTC),
            )
        )

    def list_notifications(self) -> list[Notification]:
        return list(self._notifications)