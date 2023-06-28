import re
from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.app.routers import routers
from src.app.schemas import CreateUser, ViewUser, CreateEventGroup, ViewEventGroup
from src.config import settings
from src.repositories.dependencies import Dependencies
from src.repositories.users import SqlUserRepository, PredefinedGroupsRepository
from src.storages.sql import SQLAlchemyStorage


def generate_unique_operation_id(route: APIRoute) -> str:
    # Better names for operationId in OpenAPI schema.
    # It is needed because clients generate code based on these names.
    # Requires pair (tag name + function name) to be unique.
    # See fastapi.utils:generate_unique_id (default implementation).
    operation_id = f"{route.tags[0]}_{route.name}".lower()
    operation_id = re.sub(r"\W+", "_", operation_id)
    return operation_id


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    servers=[
        {"url": "", "description": "Current"},
        {"url": "https://api.innohassle.ru", "description": "Production environment"},
    ],
    root_path_in_servers=False,
    generate_unique_id_function=generate_unique_operation_id,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY.get_secret_value()
)


@app.on_event("startup")
async def setup_repositories():
    storage = SQLAlchemyStorage.from_url(settings.DB_URL.get_secret_value())
    user_repository = SqlUserRepository(storage)
    Dependencies.set_storage(storage)
    Dependencies.set_user_repository(user_repository)

    await storage.create_all()

    groups_repository = PredefinedGroupsRepository(settings.PREDEFINED_GROUPS_FILE)
    unique_groups = groups_repository.get_unique_groups()
    db_groups = await user_repository.batch_create_group_if_not_exists(
        [CreateEventGroup(**group.dict()) for group in unique_groups]
    )
    name_x_group = {group.name: group for group in db_groups}
    users = groups_repository.get_users()
    db_users = await user_repository.batch_create_user_if_not_exists(
        [CreateUser(**user.dict()) for user in users]
    )
    user_id_x_group_ids = dict()
    for i, user in enumerate(db_users):
        schema_user = users[i]
        user_groups = [name_x_group[group.name].id for group in schema_user.groups]
        user_id_x_group_ids[user.id] = user_groups
    await user_repository.batch_setup_groups(user_id_x_group_ids)


@app.on_event("shutdown")
async def close_connection():
    storage = Dependencies.get_storage()
    await storage.close_connection()


for router in routers:
    app.include_router(router)


class VersionInfo(BaseModel):
    title = settings.APP_TITLE
    description = settings.APP_DESCRIPTION
    version = settings.APP_VERSION


@app.get("/", tags=["System"])
async def version() -> VersionInfo:
    return VersionInfo()
