__all__ = ["SqlTagRepository"]


from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


from src.app.tags.schemas import ViewTag, CreateTag
from src.repositories.tags.abc import AbstractTagRepository
from src.storages.sql import AbstractSQLAlchemyStorage
from src.storages.sql.models import Tag


class SqlTagRepository(AbstractTagRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    async def get_tag(self, tag_id: int) -> ViewTag:
        async with self.storage.create_session() as session:
            q = select(Tag).where(Tag.id == tag_id)
            tag = await session.scalar(q)

            if tag:
                return ViewTag.from_orm(tag)

    async def get_all_tags(self) -> list["ViewTag"]:
        async with self.storage.create_session() as session:
            q = select(Tag)
            r = await session.execute(q)
            return [ViewTag.from_orm(tag) for tag in r.scalars().all()]

    async def create_tag_if_not_exists(self, tag: CreateTag) -> ViewTag:
        async with self.storage.create_session() as session:
            q = insert(Tag).values(**tag.dict()).returning(Tag)
            q = q.on_conflict_do_update(
                set_={"id": Tag.id},
            )
            tag = await session.scalar(q)
            await session.commit()
            return ViewTag.from_orm(tag)

    async def batch_create_tag_if_not_exists(
        self, tags: list[CreateTag]
    ) -> list[ViewTag]:
        async with self.storage.create_session() as session:
            q = insert(Tag).values([tag.dict() for tag in tags]).returning(Tag)
            q = q.on_conflict_do_update(
                set_={"id": Tag.id},
            )
            db_tags = await session.scalars(q)
            await session.commit()
            return [ViewTag.from_orm(tag) for tag in db_tags]
