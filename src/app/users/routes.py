from fastapi import APIRouter

from src.app.dependencies import (
    EVENT_GROUP_REPOSITORY_DEPENDENCY,
    USER_REPOSITORY_DEPENDENCY,
    CURRENT_USER_ID_DEPENDENCY,
)
from src.app.schemas import ViewUser
from src.exceptions import (
    UserNotFoundException,
    DBEventGroupDoesNotExistInDb,
    EventGroupNotFoundException,
)

router = APIRouter(prefix="/users", tags=["Users"])

auth_responses_schema = {
    401: {"description": "No credentials provided"},
    403: {"description": "Could not validate credentials"},
}


@router.get(
    "/me",
    responses={
        200: {"description": "Current user info", "model": ViewUser},
        **auth_responses_schema,
    },
)
async def get_me(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    user_repository: USER_REPOSITORY_DEPENDENCY,
) -> ViewUser:
    """
    Get current user info if authenticated
    """
    return await user_repository.get_user(user_id)


@router.post(
    "/me/favorites",
    responses={
        200: {"description": "Favorite added successfully"},
        404: {"description": "Event group not found"},
        **auth_responses_schema,
    },
)
async def add_favorite(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    user_repository: USER_REPOSITORY_DEPENDENCY,
    group_id: int,
) -> ViewUser:
    """
    Add favorite to current user
    """
    try:
        updated_user = await user_repository.add_favorite(user_id, group_id)
        updated_user: ViewUser
        return updated_user
    except DBEventGroupDoesNotExistInDb as e:
        raise EventGroupNotFoundException() from e


@router.delete(
    "/me/favorites",
    responses={
        200: {"description": "Favorite deleted"},
        **auth_responses_schema,
    },
)
async def delete_favorite(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    user_repository: USER_REPOSITORY_DEPENDENCY,
    group_id: int,
) -> ViewUser:
    """
    Delete favorite from current user
    """
    updated_user = await user_repository.remove_favorite(user_id, group_id)
    updated_user: ViewUser
    return updated_user


@router.post(
    "/me/favorites/hide",
    responses={
        200: {"description": "Favorite hidden"},
        **auth_responses_schema,
    },
)
async def hide_favorite(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
    group_id: int,
    hide: bool = True,
) -> ViewUser:
    """
    Hide favorite from current user
    """
    # check if a group exists
    if await event_group_repository.get_group(group_id) is None:
        raise UserNotFoundException()

    updated_user = await event_group_repository.set_hidden(
        user_id=user_id, group_id=group_id, hide=hide, is_favorite=True
    )
    updated_user: ViewUser

    return updated_user


@router.post(
    "/me/groups/hide",
    responses={
        200: {"description": "Group hidden"},
        **auth_responses_schema,
    },
)
async def hide_group(
    user_id: CURRENT_USER_ID_DEPENDENCY,
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
    group_id: int,
    hide: bool = True,
) -> ViewUser:
    """
    Hide group from current user
    """

    # check if a group exists
    if await event_group_repository.get_group(group_id) is None:
        raise EventGroupNotFoundException()

    updated_user = await event_group_repository.set_hidden(
        user_id=user_id, group_id=group_id, hide=hide, is_favorite=False
    )
    updated_user: ViewUser

    return updated_user
