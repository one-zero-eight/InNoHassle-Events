__all__ = ["AbstractUserRepository"]

from abc import ABCMeta, abstractmethod
from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from src.app.schemas import CreateUser, ViewUser
    from src.storages.sql.models import UserXGroup

USER_ID = Annotated[int, "User ID"]


class AbstractUserRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create_user_if_not_exists(self, user: "CreateUser") -> "ViewUser":
        ...

    @abstractmethod
    async def upsert_user(self, user: "CreateUser") -> "ViewUser":
        ...

    @abstractmethod
    async def batch_create_user_if_not_exists(
        self, users: list["CreateUser"]
    ) -> list["ViewUser"]:
        ...

    @abstractmethod
    async def get_user_id_by_email(self, email: str) -> USER_ID:
        ...

    @abstractmethod
    async def get_user(self, user_id: USER_ID) -> "ViewUser":
        ...

    @abstractmethod
    async def batch_get_user(self, ids: list[USER_ID]) -> list["ViewUser"]:
        ...

    @abstractmethod
    async def add_favorite(
        self, user_id: USER_ID, favorite_id: int
    ) -> list["UserXGroup"]:
        ...

    @abstractmethod
    async def remove_favorite(
        self, user_id: USER_ID, favorite_id: int
    ) -> list["UserXGroup"]:
        ...
