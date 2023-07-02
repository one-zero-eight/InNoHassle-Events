from typing import Optional, Iterable

from pydantic import BaseModel, Json, validator
import json


class CreateEventGroup(BaseModel):
    """
    Represents a group instance to be created.
    """

    path: str
    name: Optional[str] = None
    type: Optional[str] = None
    satellite: Optional[Json] = None

    @validator("satellite", pre=True, always=True)
    def _validate_satellite(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v


class ViewEventGroup(BaseModel):
    """
    Represents a group instance from the database excluding sensitive information.
    """

    id: int
    path: str
    name: Optional[str] = None
    type: Optional[str] = None
    satellite: Optional[dict] = None

    @validator("satellite", pre=True, always=True)
    def _validate_satellite(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

    class Config:
        orm_mode = True


class UserXGroupView(BaseModel):
    """
    Represents a group instance from the database excluding sensitive information.
    """

    user_id: int
    group: ViewEventGroup
    hidden: bool

    class Config:
        orm_mode = True


class ListEventGroupsResponse(BaseModel):
    """
    Represents a list of event groups.
    """

    groups: list[ViewEventGroup]

    @classmethod
    def from_iterable(
        cls, groups: Iterable[ViewEventGroup]
    ) -> "ListEventGroupsResponse":
        return cls(groups=groups)
