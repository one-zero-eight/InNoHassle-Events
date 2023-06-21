__all__ = []

from fastapi import status, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.app.auth import router
from src.app.auth.jwt import create_access_token, Token
from src.config import settings, Environment

enabled = (
    bool(settings.DEV_AUTH_EMAIL) and settings.ENVIRONMENT == Environment.DEVELOPMENT
)
redirect_uri = settings.AUTH_REDIRECT_URI_PREFIX + "/dev"

if enabled:
    print(
        "WARNING: Dev auth provider is enabled! "
        "Use this only for development environment "
        "(otherwise, set ENVIRONMENT=production)."
    )


def check_enabled():
    if not enabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auth provider is not enabled",
        )


@router.get("/dev/login")
async def login_via_dev(request: Request):
    check_enabled()
    url = redirect_uri
    if request.query_params.get("user_id", None):
        url += "?user_id=" + request.query_params.get("user_id")
    return RedirectResponse(redirect_uri, status_code=302)


@router.get("/dev/token")
async def auth_via_dev(request: Request) -> Token:
    check_enabled()
    user_id = request.query_params.get("user_id", settings.DEV_AUTH_EMAIL)
    return create_access_token(user_id)
