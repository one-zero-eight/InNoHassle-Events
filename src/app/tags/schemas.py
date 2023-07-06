from typing import Optional, Iterable

from pydantic import BaseModel


class CreateTag(BaseModel):
    """
    Represents a group instance to be created.
    """

    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class ViewTag(BaseModel):
    """
    Represents a tag instance from the database.
    """

    id: int
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class ListOfTagsResponse(BaseModel):
    """
    Represents a list of tags.
    """

    tags: list[ViewTag]

    @classmethod
    def from_iterable(cls, tags: Iterable[ViewTag]) -> "ListOfTagsResponse":
        return cls(tags=tags)
