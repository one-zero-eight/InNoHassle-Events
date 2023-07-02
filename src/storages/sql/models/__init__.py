from src.storages.sql.models.base import Base

import src.storages.sql.models.users
import src.storages.sql.models.event_groups

from src.storages.sql.models.users import User
from src.storages.sql.models.event_groups import EventGroup, UserXFavorite, UserXGroup

all_models = [User, EventGroup]

__all__ = [*all_models, Base, UserXFavorite, UserXGroup]
