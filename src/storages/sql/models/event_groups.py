from typing import Any, TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storages.sql.models import Base

if TYPE_CHECKING:
    from src.storages.sql.models.users import User


class EventGroup(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(nullable=True)
    satellite: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)


class UserXFavorite(Base):
    __tablename__ = "users_x_favorites"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    hidden: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship("User", back_populates="favorites_association")
    group: Mapped[EventGroup] = relationship(lazy="joined")


class UserXGroup(Base):
    __tablename__ = "users_x_groups"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    hidden: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship("User", back_populates="groups_association")
    group: Mapped[EventGroup] = relationship(lazy="joined")
