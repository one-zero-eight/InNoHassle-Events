__all__ = [
    "STORAGE_DEPENDENCY",
    "USER_REPOSITORY_DEPENDENCY",
    "EVENT_GROUP_REPOSITORY_DEPENDENCY",
    "CURRENT_USER_ID_DEPENDENCY",
    "IS_VERIFIED_PARSER_DEPENDENCY",
    "Dependencies",
]

from typing import Annotated, Callable

from fastapi import Depends

from src.repositories.event_groups import AbstractEventGroupRepository
from src.repositories.tags import AbstractTagRepository
from src.repositories.users import AbstractUserRepository
from src.storages.sql.storage import AbstractSQLAlchemyStorage


class Dependencies:
    _storage: "AbstractSQLAlchemyStorage"
    _user_repository: "AbstractUserRepository"
    _event_group_repository: "AbstractEventGroupRepository"
    _tag_repository: "AbstractTagRepository"

    @classmethod
    def get_storage(cls) -> "AbstractSQLAlchemyStorage":
        return cls._storage

    @classmethod
    def set_storage(cls, storage: "AbstractSQLAlchemyStorage"):
        cls._storage = storage

    @classmethod
    def get_user_repository(cls) -> "AbstractUserRepository":
        return cls._user_repository

    @classmethod
    def set_user_repository(cls, user_repository: "AbstractUserRepository"):
        cls._user_repository = user_repository

    @classmethod
    def get_event_group_repository(cls) -> "AbstractEventGroupRepository":
        return cls._event_group_repository

    @classmethod
    def set_event_group_repository(cls, event_group_repository: "AbstractEventGroupRepository"):
        cls._event_group_repository = event_group_repository

    @classmethod
    def get_tag_repository(cls) -> "AbstractTagRepository":
        return cls._tag_repository

    @classmethod
    def set_tag_repository(cls, tag_repository: "AbstractTagRepository"):
        cls._tag_repository = tag_repository

    get_current_user_id: Callable[..., str]

    is_verified_parser: Callable[..., bool]


STORAGE_DEPENDENCY = Annotated[AbstractSQLAlchemyStorage, Depends(Dependencies.get_storage)]
USER_REPOSITORY_DEPENDENCY = Annotated[AbstractUserRepository, Depends(Dependencies.get_user_repository)]
EVENT_GROUP_REPOSITORY_DEPENDENCY = Annotated[
    AbstractEventGroupRepository, Depends(Dependencies.get_event_group_repository)
]
TAG_REPOSITORY_DEPENDENCY = Annotated[AbstractTagRepository, Depends(Dependencies.get_tag_repository)]

from src.app.auth.dependencies import get_current_user_id, is_verified_parser  # noqa: E402

Dependencies.get_current_user_id = get_current_user_id
Dependencies.is_verified_parser = is_verified_parser

CURRENT_USER_ID_DEPENDENCY = Annotated[str, Depends(Dependencies.get_current_user_id)]
IS_VERIFIED_PARSER_DEPENDENCY = Annotated[bool, Depends(Dependencies.is_verified_parser)]
