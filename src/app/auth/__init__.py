__all__ = ["oauth", "router"]

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth = OAuth()

# Register all OAuth applications and routes
import src.app.auth.common  # noqa
import src.app.auth.innopolis  # noqa
import src.app.auth.dev  # noqa
