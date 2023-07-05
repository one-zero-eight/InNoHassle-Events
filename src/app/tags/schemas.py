from typing import Optional

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
