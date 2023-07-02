__all__ = ["get_current_user_email"]

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyCookie

from src.app.auth.jwt import verify_token
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
    name="token",  # Cookie name
    auto_error=False,  # We'll handle error manually
)


def get_current_user_email(
    bearer: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    cookie: str = Depends(cookie_scheme),
) -> str:
    # Prefer header to cookie
    token = (bearer and bearer.credentials) or cookie
    if not token:
        raise NoCredentialsException()

    token_data = verify_token(token, IncorrectCredentialsException())
    return token_data.email
