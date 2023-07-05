from abc import ABCMeta, abstractmethod

from src.app.tags.schemas import ViewTag, CreateTag


class AbstractTagRepository(metaclass=ABCMeta):

    @abstractmethod
    async def get_tag(self, tag_id: int) -> ViewTag:
        ...

    @abstractmethod
    async def get_all_tags(self) -> list["ViewTag"]:
        ...

    @abstractmethod
    async def create_tag_if_not_exists(self, tag: CreateTag) -> ViewTag:
        ...

    @abstractmethod
    async def batch_create_tag_if_not_exists(self, tags: list[CreateTag]) -> list[ViewTag]:
        ...
