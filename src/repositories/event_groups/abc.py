__all__ = ["AbstractEventGroupRepository"]

from abc import ABCMeta, abstractmethod
from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from src.app.schemas import CreateEventGroup, ViewEventGroup, ViewUser

USER_ID = Annotated[int, "User ID"]


class AbstractEventGroupRepository(metaclass=ABCMeta):
    @abstractmethod
    async def setup_groups(self, user_id: USER_ID, groups: list[int]):
        ...

    @abstractmethod
    async def batch_setup_groups(self, groups_mapping: dict[USER_ID, list[int]]):
        ...

    @abstractmethod
    async def get_group(self, group_id: int) -> "ViewEventGroup":
        ...

    @abstractmethod
    async def get_group_by_path(self, path: str) -> "ViewEventGroup":
        ...

    @abstractmethod
    async def create_group_if_not_exists(
            self, group: "CreateEventGroup"
    ) -> "ViewEventGroup":
        ...

    @abstractmethod
    async def batch_create_group_if_not_exists(
            self, groups: list["CreateEventGroup"]
    ) -> list["ViewEventGroup"]:
        ...

    @abstractmethod
    async def get_all_groups(self) -> "ViewUser":
        ...

    @abstractmethod
    async def set_hidden(
            self, user_id: USER_ID, is_favorite: bool, group_id: int, hide: bool = True
    ) -> "ViewUser":
        ...
