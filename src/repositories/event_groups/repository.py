__all__ = ["SqlEventGroupRepository"]

from typing import Annotated

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

from src.app.event_groups.schemas import (
    UserXGroupView,
    ViewEventGroup,
    CreateEventGroup,
)
from src.repositories.event_groups.abc import AbstractEventGroupRepository
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
                select(User)
                .where(User.id == user_id)
                .options(
                    selectinload(User.favorites_association),
                    selectinload(User.groups_association),
                )
            )

            user = await session.scalar(q)
            user: User

            group_objs = await session.execute(
                select(EventGroup).where(EventGroup.id.in_(groups))
            )

            group_scalars = group_objs.scalars().all()
            user.groups = group_scalars
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
            q = q.on_conflict_do_nothing(
                index_elements=[UserXGroup.user_id, UserXGroup.group_id]
            )
            await session.execute(q)
            await session.commit()

    async def set_hidden(
        self, user_id: USER_ID, is_favorite: bool, group_id: int, hide: bool = True
    ) -> list[UserXGroupView]:
        async with self.storage.create_session() as session:
            table = UserXFavorite if is_favorite else UserXGroup
            table: UserXFavorite | UserXGroup

            query = (
                update(table)
                .where(table.user_id == user_id)
                .where(table.group_id == group_id)
                .values(hidden=hide)
            )
            await session.execute(query)
            await session.commit()

            # from table
            q = select(table).where(table.user_id == user_id)

            groups = await session.execute(q)
            return [UserXGroupView.from_orm(group) for group in groups.scalars().all()]

    async def get_group(self, group_id: int) -> ViewEventGroup:
        async with self.storage.create_session() as session:
            q = select(EventGroup).where(EventGroup.id == group_id)
            group = await session.scalar(q)

            if group:
                return ViewEventGroup.from_orm(group)

    async def get_all_groups(self) -> list["ViewEventGroup"]:
        async with self.storage.create_session() as session:
            q = select(EventGroup)
            r = await session.execute(q)
            return [ViewEventGroup.from_orm(group) for group in r.scalars().all()]

    async def get_group_by_path(self, path: str) -> ViewEventGroup:
        async with self.storage.create_session() as session:
            q = select(EventGroup).where(EventGroup.path == path)
            group = await session.scalar(q)

            if group:
                return ViewEventGroup.from_orm(group)

    async def create_group_if_not_exists(
        self, group: CreateEventGroup
    ) -> ViewEventGroup:
        async with self.storage.create_session() as session:
            q = insert(EventGroup).values(**group.dict()).returning(EventGroup)
            q = q.on_conflict_do_update(
                index_elements=[EventGroup.path],
                set_={"id": EventGroup.id},
            )
            group = await session.scalar(q)
            await session.commit()
            return ViewEventGroup.from_orm(group)

    async def batch_create_group_if_not_exists(
        self, groups: list[CreateEventGroup]
    ) -> list[ViewEventGroup]:
        async with self.storage.create_session() as session:
            q = (
                insert(EventGroup)
                .values([group.dict() for group in groups])
                .returning(EventGroup)
            )
            q = q.on_conflict_do_update(
                index_elements=[EventGroup.path],
                set_={"id": EventGroup.id},
            )
            db_groups = await session.scalars(q)
            await session.commit()
            return [ViewEventGroup.from_orm(group) for group in db_groups]
