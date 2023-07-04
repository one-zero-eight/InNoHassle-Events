from fastapi import HTTPException
from starlette import status


class NoCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No credentials provided",
            headers={"WWW-Authenticate": "Bearer"},
        )


class IncorrectCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


class EventGroupNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event group not found",
        )


class DBException(Exception):
    ...


class DBEventGroupDoesNotExistInDb(DBException):
    def __init__(self, id: int):
        super().__init__(f"Event group with id {id} does not exist in db")
