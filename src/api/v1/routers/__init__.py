from .authorization import router as v1_authorization_router
from .division import router as v1_division_router
from .position import router as v1_position_router
from .registration import router as v1_registration_router
from .tasks import router as v1_tasks_router
from .users import router as v1_users_router

__all__ = [
    "v1_authorization_router",
    "v1_division_router",
    "v1_position_router",
    "v1_registration_router",
    "v1_tasks_router",
    "v1_users_router",
]
