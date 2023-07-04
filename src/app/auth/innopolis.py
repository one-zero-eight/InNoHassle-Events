__all__ = []

from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field
from starlette.requests import Request

from src.app.auth import router, oauth
from src.app.auth.common import redirect_with_token
from src.app.dependencies import Dependencies
from src.app.auth.jwt import create_access_token
from src.app.users.schemas import CreateUser
from src.config import settings
from src.repositories.users.abc import AbstractUserRepository


class UserInfoFromSSO(BaseModel):
    email: str
    name: str | None = Field(alias="commonname")
    status: str | None = Field(alias="Status")


enabled = bool(settings.INNOPOLIS_SSO_CLIENT_ID.get_secret_value())
redirect_uri = settings.INNOPOLIS_SSO_REDIRECT_URI

if enabled:
    innopolis_sso = oauth.register(
        "innopolis",
        client_id=settings.INNOPOLIS_SSO_CLIENT_ID.get_secret_value(),
        client_secret=settings.INNOPOLIS_SSO_CLIENT_SECRET.get_secret_value(),
        # OAuth client will fetch configuration on first request
        server_metadata_url="https://sso.university.innopolis.ru/adfs/.well-known/openid-configuration",
        client_kwargs={"scope": "openid"},
    )

    @router.get("/innopolis/login", include_in_schema=False)
    async def innopolis_login(return_to: str, request: Request):
        request.session.clear()  # Clear session cookie as it is used only during authentication
        request.session["return_to"] = return_to
        return await oauth.innopolis.authorize_redirect(request, redirect_uri)

    @router.get("/innopolis/callback", include_in_schema=False)
    async def innopolis_callback(
        request: Request,
        user_repository: Annotated[
            AbstractUserRepository, Depends(Dependencies.get_user_repository)
        ],
    ):
        token = await oauth.innopolis.authorize_access_token(request)
        user_info_dict: dict = token["userinfo"]
        user_info = UserInfoFromSSO(**user_info_dict)
        user = await user_repository.upsert_user(CreateUser(**user_info.dict()))

        return_to = request.session.pop("return_to")
        request.session.clear()  # Clear session cookie as it is used only during authentication
        token = create_access_token(user.id)
        return redirect_with_token(return_to, token)
