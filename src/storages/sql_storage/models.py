from sqlalchemy import Table, Column, String, MetaData, ForeignKey

metadata = MetaData()


class User:
    email = Column("email", String, primary_key=True)
    ru_name = Column("ru_name", String)
    common_name = Column("common_name", String)
    status = Column("status", String)
    favorites = Column("favorites", String)
    groups = Column("groups", String)


group = Table("group", metadata, Column("name", String), Column("type", String))

user = Table(
    "user",
    metadata,
    Column("email", String, primary_key=True),
    Column("ru_name", String),
    Column("common_name", String),
    Column("status", String),
    Column("favorites", String),
    Column("groups", String, ForeignKey(group.c.name)),
)
