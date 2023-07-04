__all__ = []

from typing import Optional, Annotated

from fastapi import Depends

from src.app.auth import router
from src.app.auth.common import redirect_with_token
from src.app.auth.jwt import create_access_token
from src.app.users.schemas import CreateUser
from src.config import settings, Environment
from src.app.dependencies import Dependencies
from src.repositories.users import AbstractUserRepository

enabled = (
    bool(settings.DEV_AUTH_EMAIL) and settings.ENVIRONMENT == Environment.DEVELOPMENT
)

if enabled:
    print(
        "WARNING: Dev auth provider is enabled! "
        "Use this only for development environment "
        "(otherwise, set ENVIRONMENT=production)."
    )

    @router.get("/dev/login", include_in_schema=False)
    async def dev_login(
        user_repository: Annotated[
            AbstractUserRepository, Depends(Dependencies.get_user_repository)
        ],
        return_to: str = "/",
        email: Optional[str] = None,
    ):
        email = email or settings.DEV_AUTH_EMAIL
        user = await user_repository.upsert_user(
            CreateUser(email=email, name="Ivan Petrov", status="Student")
        )
        token = create_access_token(user.id)
        return redirect_with_token(return_to, token)

    @router.get("/dev/token")
    async def get_dev_token(
        user_repository: Annotated[
            AbstractUserRepository, Depends(Dependencies.get_user_repository)
        ],
        email: Optional[str] = None,
    ) -> str:
        email = email or settings.DEV_AUTH_EMAIL
        user = await user_repository.upsert_user(
            CreateUser(email=email, name="Ivan Petrov", status="Student")
        )
        return create_access_token(user.id)
