from src.storages.sql.models.base import Base

from src.storages.sql.models.users import User
from src.storages.sql.models.event_groups import EventGroup, UserXFavorite, UserXGroup

all_models = [User, EventGroup, UserXFavorite, UserXGroup]

__all__ = [*all_models, Base]
