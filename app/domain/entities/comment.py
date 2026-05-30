from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class Comment:
    id: str
    task_id: str
    author_id: str
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.task_id = self.task_id.strip()
        self.author_id = self.author_id.strip()
        self.content = self.content.strip()

        if not self.id:
            raise ValueError("Comment id must not be empty.")
        if not self.task_id:
            raise ValueError("Comment task id must not be empty.")
        if not self.author_id:
            raise ValueError("Comment author id must not be empty.")
        if not self.content:
            raise ValueError("Comment content must not be empty.")

    def edit(self, new_content: str) -> None:
        sanitized_content = new_content.strip()
        if not sanitized_content:
            raise ValueError("Comment content must not be empty.")
        self.content = sanitized_content
        self.updated_at = datetime.now(UTC)
