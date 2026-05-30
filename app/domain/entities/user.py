from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class User:
    id: str
    name: str
    email: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.name = self.name.strip()
        self.email = self.email.strip().lower()

        if not self.id:
            raise ValueError("User id must not be empty.")
        if not self.name:
            raise ValueError("User name must not be empty.")
        if "@" not in self.email:
            raise ValueError("User email must be valid.")

    def rename(self, new_name: str) -> None:
        sanitized_name = new_name.strip()
        if not sanitized_name:
            raise ValueError("User name must not be empty.")
        self.name = sanitized_name

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True
