__all__ = ["SqlEventGroupRepository"]

from typing import Annotated

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload

from src.repositories.event_groups.abc import AbstractEventGroupRepository
from src.schemas import ViewEventGroup, CreateEventGroup, ViewUser
from src.storages.sql import AbstractSQLAlchemyStorage
from src.storages.sql.models import UserXFavorite, UserXGroup, EventGroup, User

USER_ID = Annotated[int, "User ID"]


class SqlEventGroupRepository(AbstractEventGroupRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    async def setup_groups(self, user_id: USER_ID, groups: list[int]):
        async with self.storage.create_session() as session:
            q = (
                insert(UserXGroup)
                .values([{"user_id": user_id, "group_id": group_id} for group_id in groups])
                .on_conflict_do_nothing(index_elements=[UserXGroup.user_id, UserXGroup.group_id])
            )
            await session.execute(q)
            await session.commit()

    async def batch_setup_groups(self, groups_mapping: dict[USER_ID, list[int]]):
        async with self.storage.create_session() as session:
            # in one query
            q = insert(UserXGroup).values(
                [
                    {"user_id": user_id, "group_id": group_id}
                    for user_id, group_ids in groups_mapping.items()
                    for group_id in group_ids
                ]
            )
            q = q.on_conflict_do_nothing(index_elements=[UserXGroup.user_id, UserXGroup.group_id])
            await session.execute(q)
            await session.commit()

    async def set_hidden(self, user_id: USER_ID, group_id: int, hide: bool = True) -> "ViewUser":
        async with self.storage.create_session() as session:
            # find favorite where user_id and group_id
            q = select(UserXFavorite).where(UserXFavorite.user_id == user_id).where(UserXFavorite.group_id == group_id)

            event_group = await session.scalar(q)

            # if not found, then it should be in groups

            if not event_group:
                q = select(UserXGroup).where(UserXGroup.user_id == user_id).where(UserXGroup.group_id == group_id)
                event_group = await session.scalar(q)

            # set hidden
            if event_group:
                event_group.hidden = hide

            # from table
            q = (
                select(User)
                .where(User.id == user_id)
                .options(
                    joinedload(User.favorites_association),
                    joinedload(User.groups_association),
                )
            )
            user = await session.scalar(q)
            await session.commit()
            return ViewUser.from_orm(user)

    async def get_group(self, group_id: int) -> ViewEventGroup:
        async with self.storage.create_session() as session:
            q = select(EventGroup).where(EventGroup.id == group_id)
            group = await session.scalar(q)

            if group:
                return ViewEventGroup.from_orm(group)

    async def get_all_groups(self) -> list["ViewEventGroup"]:
        async with self.storage.create_session() as session:
            q = select(EventGroup).order_by(EventGroup.path)
            r = await session.execute(q)
            return [ViewEventGroup.from_orm(group) for group in r.scalars().all()]

    async def get_group_by_path(self, path: str) -> ViewEventGroup:
        async with self.storage.create_session() as session:
            q = select(EventGroup).where(EventGroup.path == path)
            group = await session.scalar(q)

            if group:
                return ViewEventGroup.from_orm(group)

    async def create_group_if_not_exists(self, group: CreateEventGroup) -> ViewEventGroup:
        async with self.storage.create_session() as session:
            q = insert(EventGroup).values(**group.dict()).returning(EventGroup)
            q = q.on_conflict_do_update(
                index_elements=[EventGroup.path],
                set_={"id": EventGroup.id},
            )
            group = await session.scalar(q)
            await session.commit()
            return ViewEventGroup.from_orm(group)

    async def batch_create_group_if_not_exists(self, groups: list[CreateEventGroup]) -> list[ViewEventGroup]:
        async with self.storage.create_session() as session:
            q = insert(EventGroup).values([group.dict() for group in groups]).returning(EventGroup)
            q = q.on_conflict_do_update(
                index_elements=[EventGroup.path],
                set_={"id": EventGroup.id},
            )
            db_groups = await session.scalars(q)
            await session.commit()
            return [ViewEventGroup.from_orm(group) for group in db_groups]
