__all__ = ["create_access_token", "verify_token", "TokenData"]

from datetime import timedelta, datetime
from typing import Optional

from jose import JWTError, jwt
from pydantic import BaseModel

from src.config import settings

ALGORITHM = "HS256"


class TokenData(BaseModel):
    email: Optional[str] = None


def create_access_token(email: str) -> str:
    access_token = _create_access_token(
        data={"sub": email},
        expires_delta=timedelta(days=90),
    )
    return access_token


def _create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY.get_secret_value(), algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY.get_secret_value(), algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception
