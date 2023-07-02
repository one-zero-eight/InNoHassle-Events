__all__ = ["PredefinedGroupsRepository"]

import json
from pathlib import Path
from typing import Optional, Any

from pydantic import BaseModel, Field
from pydantic import validator, parse_obj_as


class InJsonEventGroup(BaseModel):
    """
    Represents a group instance from the predefined users json file.
    """

    name: Optional[str]
    type: Optional[str]
    path: str


class InJsonUser(BaseModel):
    """
    Represents a user instance from the predefined users json file.
    """

    email: str
    groups: list[InJsonEventGroup] = Field(default_factory=list)


class PredefinedGroup(BaseModel):
    name: Optional[str]
    type: Optional[str]
    path: str
    satellite: Optional[dict[str, Any]]


class JsonUserStorage(BaseModel):
    users: list[InJsonUser] = Field(default_factory=list)

    @validator("users", pre=True, each_item=True, always=True)
    def _validate_user(cls, v):
        if isinstance(v, dict):
            return InJsonUser(**v)
        return v


class JsonGroupStorage(BaseModel):
    groups: list[PredefinedGroup] = Field(default_factory=list)

    @validator("groups", pre=True, each_item=True, always=True)
    def _validate_group(cls, v):
        if isinstance(v, dict):
            return PredefinedGroup(**v)
        return v


class PredefinedGroupsRepository:
    user_storage: JsonUserStorage
    event_group_storage: JsonGroupStorage

    def __init__(self, user_file: Path, event_group_file: Path):
        self.user_storage = self._load_users(user_file)
        self.event_group_storage = self._load_groups(event_group_file)

    @staticmethod
    def _load_users(file_path: Path) -> JsonUserStorage:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                users_dict = json.load(f)
        except FileNotFoundError:
            # create empty file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write('{"users": []}')
            return JsonUserStorage()
        return parse_obj_as(JsonUserStorage, users_dict)

    @staticmethod
    def _load_groups(file_path: Path) -> JsonGroupStorage:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                groups_dict = json.load(f)
        except FileNotFoundError:
            # create empty file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write('{"groups": []}')
            return JsonGroupStorage()
        return parse_obj_as(JsonGroupStorage, groups_dict)

    def get_users(self) -> list[InJsonUser]:
        return self.user_storage.users.copy()

    def get_groups(self) -> list[PredefinedGroup]:
        return self.event_group_storage.groups.copy()
