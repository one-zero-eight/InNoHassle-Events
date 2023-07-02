from fastapi import APIRouter

from src.app.dependencies import EVENT_GROUP_REPOSITORY_DEPENDENCY
from src.app.event_groups.schemas import ViewEventGroup, ListEventGroupsResponse
from src.exceptions import EventGroupNotFoundException

router = APIRouter(prefix="/event-groups", tags=["Event Groups"])


@router.get(
    "/by-path",
    responses={
        200: {"description": "Event group info", "model": ViewEventGroup},
        404: {"description": "Event group not found"},
    },
)
async def find_event_group_by_path(
    path: str,
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
) -> ViewEventGroup:
    """
    Get event group info by path
    """

    event_group = await event_group_repository.get_group_by_path(path)

    if event_group is None:
        raise EventGroupNotFoundException()
    return event_group


@router.get(
    "/{event_group_id}",
    responses={
        200: {"description": "Event group info", "model": ViewEventGroup},
        404: {"description": "Event group not found"},
    },
)
async def get_event_group(
    event_group_id: int,
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
) -> ViewEventGroup:
    """
    Get event group info by id
    """
    event_group = await event_group_repository.get_group(event_group_id)

    if event_group is None:
        raise EventGroupNotFoundException()

    return event_group


@router.get(
    "/",
    responses={
        200: {"description": "List of event groups", "model": ListEventGroupsResponse},
    },
)
async def list_event_groups(
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
) -> ListEventGroupsResponse:
    """
    Get a list of all event groups
    """
    groups = await event_group_repository.get_all_groups()
    return ListEventGroupsResponse.from_iterable(groups)
