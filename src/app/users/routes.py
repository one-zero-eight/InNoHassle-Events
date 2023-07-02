from typing import Iterable

from fastapi import APIRouter
from pydantic import BaseModel

from src.app.dependencies import (
    EVENT_GROUP_REPOSITORY_DEPENDENCY,
    USER_REPOSITORY_DEPENDENCY,
    CURRENT_USER_EMAIL_DEPENDENCY,
)
from src.app.schemas import ViewUser, UserXGroupView
from src.exceptions import UserNotFoundException

router = APIRouter(prefix="/users", tags=["Users"])

auth_responses_schema = {
    401: {"description": "User is not authenticated"},
    404: {"description": "User not found"},
}


@router.get(
    "/me",
    responses={
        200: {"description": "Current user info", "model": ViewUser},
        **auth_responses_schema,
    },
)
async def get_me(
    email: CURRENT_USER_EMAIL_DEPENDENCY,
    user_repository: USER_REPOSITORY_DEPENDENCY,
) -> ViewUser:
    """
    Get current user info if authenticated
    """
    user_id = await user_repository.get_user_id_by_email(email)

    if user_id is None:
        raise UserNotFoundException()

    return await user_repository.get_user(user_id)


class ListOfFavorites(BaseModel):
    favorites: list[UserXGroupView]

    @classmethod
    def from_iterable(cls, favorites: Iterable[UserXGroupView]) -> "ListOfFavorites":
        return cls(favorites=list(favorites))


@router.post(
    "/me/favorites",
    responses={
        200: {"description": "Favorite added successfully"},
        **auth_responses_schema,
    },
)
async def add_favorite(
    email: CURRENT_USER_EMAIL_DEPENDENCY,
    user_repository: USER_REPOSITORY_DEPENDENCY,
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
    group_id: int,
) -> ListOfFavorites:
    """
    Add favorite to current user
    """
    user_id = await user_repository.get_user_id_by_email(email)

    if user_id is None:
        raise UserNotFoundException()

    group = await event_group_repository.get_group(group_id)

    if group is None:
        raise UserNotFoundException()

    updated_favorites = await user_repository.add_favorite(user_id, group.id)
    return ListOfFavorites.from_iterable(updated_favorites)


@router.delete(
    "/me/favorites",
    responses={
        200: {"description": "Favorite deleted"},
        **auth_responses_schema,
    },
)
async def delete_favorite(
    email: CURRENT_USER_EMAIL_DEPENDENCY,
    user_repository: USER_REPOSITORY_DEPENDENCY,
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
    group_id: int,
) -> ListOfFavorites:
    """
    Delete favorite from current user
    """
    user_id = await user_repository.get_user_id_by_email(email)

    if user_id is None:
        raise UserNotFoundException()

    # check if group exists
    if await event_group_repository.get_group(group_id) is None:
        raise UserNotFoundException()

    updated_favorites = await user_repository.remove_favorite(user_id, group_id)
    return ListOfFavorites.from_iterable(updated_favorites)


@router.post(
    "/me/favorites/hide",
    responses={
        200: {"description": "Favorite hidden"},
        **auth_responses_schema,
    },
)
async def hide_favorite(
    email: CURRENT_USER_EMAIL_DEPENDENCY,
    user_repository: USER_REPOSITORY_DEPENDENCY,
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
    group_id: int,
    hide: bool = True,
) -> ListOfFavorites:
    """
    Hide favorite from current user
    """
    user_id = await user_repository.get_user_id_by_email(email)

    if user_id is None:
        raise UserNotFoundException()

    # check if group exists
    if await event_group_repository.get_group(group_id) is None:
        raise UserNotFoundException()

    updated_favorites = await event_group_repository.set_hidden(
        user_id=user_id, group_id=group_id, hide=hide, is_favorite=True
    )

    return ListOfFavorites.from_iterable(updated_favorites)


@router.post(
    "/me/groups/hide",
    responses={
        200: {"description": "Group hidden"},
        **auth_responses_schema,
    },
)
async def hide_group(
    email: CURRENT_USER_EMAIL_DEPENDENCY,
    user_repository: USER_REPOSITORY_DEPENDENCY,
    event_group_repository: EVENT_GROUP_REPOSITORY_DEPENDENCY,
    group_id: int,
    hide: bool = True,
) -> ListOfFavorites:
    """
    Hide group from current user
    """
    user_id = await user_repository.get_user_id_by_email(email)

    if user_id is None:
        raise UserNotFoundException()

    # check if group exists
    if await event_group_repository.get_group(group_id) is None:
        raise UserNotFoundException()

    updated_favorites = await event_group_repository.set_hidden(
        user_id=user_id, group_id=group_id, hide=hide, is_favorite=False
    )

    return ListOfFavorites.from_iterable(updated_favorites)
