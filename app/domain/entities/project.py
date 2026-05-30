from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class Project:
    id: str
    name: str
    owner_id: str
    description: str = ""
    member_ids: list[str] = field(default_factory=list)
    is_archived: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        self.id = self.id.strip()
        self.name = self.name.strip()
        self.owner_id = self.owner_id.strip()
        self.description = self.description.strip()

        if not self.id:
            raise ValueError("Project id must not be empty.")
        if not self.name:
            raise ValueError("Project name must not be empty.")
        if not self.owner_id:
            raise ValueError("Project owner id must not be empty.")

        normalized_members = [member_id.strip() for member_id in self.member_ids if member_id.strip()]
        if self.owner_id not in normalized_members:
            normalized_members.append(self.owner_id)
        self.member_ids = normalized_members

    def rename(self, new_name: str) -> None:
        sanitized_name = new_name.strip()
        if not sanitized_name:
            raise ValueError("Project name must not be empty.")
        self.name = sanitized_name
        self.touch()

    def update_description(self, new_description: str) -> None:
        self.description = new_description.strip()
        self.touch()

    def add_member(self, user_id: str) -> None:
        sanitized_user_id = user_id.strip()
        if not sanitized_user_id:
            raise ValueError("Member id must not be empty.")
        if sanitized_user_id not in self.member_ids:
            self.member_ids.append(sanitized_user_id)
            self.touch()

    def remove_member(self, user_id: str) -> None:
        sanitized_user_id = user_id.strip()
        if sanitized_user_id == self.owner_id:
            raise ValueError("Project owner cannot be removed from members.")
        if sanitized_user_id in self.member_ids:
            self.member_ids.remove(sanitized_user_id)
            self.touch()

    def archive(self) -> None:
        self.is_archived = True
        self.touch()

    def restore(self) -> None:
        self.is_archived = False
        self.touch()

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC)
