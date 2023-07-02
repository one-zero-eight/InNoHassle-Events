from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from src.app.event_groups.schemas import (
    CreateEventGroup,
    ViewEventGroup,
    UserXGroupView,
)
from src.app.users.schemas import CreateUser, ViewUser

# fmt: off
all_schemas = [
    CreateUser, ViewUser,
    CreateEventGroup, ViewEventGroup, UserXGroupView,
]
# fmt: on

router = APIRouter(tags=["System"])
schema_dict = {
    schema.__name__: schema.schema(ref_template="#/components/schemas/{model}")
    for schema in all_schemas
}


class Schemas(BaseModel):
    """
    Represents a dictionary of all schemas.
    """

    schemas: dict[str, Any]


@router.get(
    "/schemas",
    response_model=Schemas,
    responses={
        200: {
            "description": "Returns a dictionary of all schemas.",
            "content": {"application/json": {"example": {"schemas": schema_dict}}},
        }
    },
)
async def schemas():
    return {"schemas": schema_dict}


__all__ = [*all_schemas, "BaseModel", "router"]
