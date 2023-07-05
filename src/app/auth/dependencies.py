__all__ = ["get_current_user_id"]

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyCookie

from src.app.auth.jwt import verify_user_token
from src.config import settings
from src.exceptions import (
    NoCredentialsException,
    IncorrectCredentialsException,
)

bearer_scheme = HTTPBearer(
    scheme_name="Bearer",
    description="Your JSON Web Token (JWT)",
    auto_error=False,  # We'll handle error manually
)

cookie_scheme = APIKeyCookie(
    scheme_name="Cookie",
    description="Your JSON Web Token (JWT) stored as 'token' cookie",
    name=settings.AUTH_COOKIE_NAME,  # Cookie name
    auto_error=False,  # We'll handle error manually
)


def get_current_user_id(
    bearer: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    cookie: str = Depends(cookie_scheme),
) -> int:
    # Prefer header to cookie
    token = (bearer and bearer.credentials) or cookie
    if not token:
        raise NoCredentialsException()

    token_data = verify_user_token(token, IncorrectCredentialsException())
    return token_data.user_id
