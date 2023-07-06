from src.app.users import router as router_users
from src.app.event_groups import router as router_event_groups
from src.app.auth import router as router_auth
from src.app.schemas import router as router_schemas
from src.app.tags import router as router_tags

routers = [router_users, router_event_groups, router_schemas, router_auth, router_tags]

__all__ = ["routers", *routers]
