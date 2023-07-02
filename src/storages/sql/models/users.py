from typing import TYPE_CHECKING

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.storages.sql.models.base import Base

if TYPE_CHECKING:
    from src.storages.sql.models.event_groups import EventGroup
    from src.storages.sql.models import UserXFavorite, UserXGroup


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)

    email: Mapped[str] = mapped_column(unique=True)

    status: Mapped[str] = mapped_column(nullable=True)
    favorites_association: Mapped[list["UserXFavorite"]] = relationship(
        "UserXFavorite",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    favorites: Mapped[list["EventGroup"]] = association_proxy(
        "favorites_association",
        "group",
        creator=lambda group: UserXFavorite(group=group),
    )

    groups_association: Mapped[list["UserXGroup"]] = relationship(
        "UserXGroup",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    groups: Mapped[list["EventGroup"]] = association_proxy(
        "groups_association", "group", creator=lambda group: UserXGroup(group=group)
    )
