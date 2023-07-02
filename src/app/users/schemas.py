from typing import Optional, Collection

from pydantic import Field, BaseModel, validator


class CreateUser(BaseModel):
    """
    Represents a user instance to be created.
    """

    email: str
    name: Optional[str] = None
    status: Optional[str] = None


class ViewUser(BaseModel):
    """
    Represents a user instance from the database excluding sensitive information.
    """

    id: int
    email: str
    name: Optional[str] = None
    status: Optional[str] = None
    groups_association: list["UserXGroupView"] = Field(default_factory=list)
    favorites_association: list["UserXGroupView"] = Field(default_factory=list)

    @validator("groups_association", "favorites_association", pre=True)
    def groups_to_list(cls, v):
        if isinstance(v, Collection):
            return list(v)
        return v

    class Config:
        orm_mode = True


# fix circular import
from src.app.event_groups.schemas import UserXGroupView

ViewUser.update_forward_refs()
