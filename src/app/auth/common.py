from datetime import datetime, timedelta, timezone

from starlette.responses import RedirectResponse

from src.app.auth import router
from src.config import settings


def redirect_with_token(return_to: str, token: str):
    response = RedirectResponse(return_to, status_code=302)
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,
        domain=settings.AUTH_COOKIE_DOMAIN,
        expires=datetime.now().astimezone(tz=timezone.utc) + timedelta(days=90),
    )
    return response


@router.get("/logout", include_in_schema=False)
async def innopolis_logout(return_to: str):
    response = RedirectResponse(return_to, status_code=302)
    response.delete_cookie(
        key="token",
        httponly=True,
        secure=True,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    return response
