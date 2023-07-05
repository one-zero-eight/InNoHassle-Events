from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storages.sql.models import Base
from src.storages.sql.models.event_groups import EventGroup


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    event_group_association: Mapped[list["TagXEventGroup"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan",
    )

    event_group: Mapped[list["EventGroup"]] = association_proxy(
        "event_group_association",
        "event_group",
        creator=lambda event_group: TagXEventGroup(event_group=event_group),
    )


class TagXEventGroup(Base):
    __tablename__ = "tags_x_event_groups"
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))
    event_group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"), primary_key=True
    )

    tag: Mapped["Tag"] = relationship("Tag", back_populates="event_group_association")
    event_group: Mapped[EventGroup] = relationship(lazy="joined")
