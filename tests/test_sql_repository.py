from unittest import mock

import pytest

from src.app.dependencies import Dependencies
from src.config import settings

from src.app.tags.schemas import CreateTag
from src.repositories.tags import SqlTagRepository
from src.storages.sql import SQLAlchemyStorage


async def test_create_tag_if_not_exists():
    storage = SQLAlchemyStorage.from_url(settings.DB_URL.get_secret_value())
    tag_repository = SqlTagRepository(storage)
    Dependencies.set_storage(storage)
    Dependencies.set_tag_repository(tag_repository)
    await tag_repository.delete_all()
    tag1 = CreateTag(name="test_name", description="test_description")
    res = await tag_repository.create_tag_if_not_exists(tag1)
    assert res.name == tag1.name
    assert res.description == tag1.description
