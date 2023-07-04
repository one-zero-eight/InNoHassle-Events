from src.storages.sql.models.base import Base

from src.storages.sql.models.users import User
from src.storages.sql.models.event_groups import EventGroup, UserXFavorite, UserXGroup
from src.storages.sql.models.tags import Tag, TagXEventGroup

all_models = [User, EventGroup, UserXFavorite, UserXGroup, Tag, TagXEventGroup]

__all__ = [*all_models, Base]
