from .authorization import router as v1_authorization_router
from .registration import router as v1_registration_router
from .users import router as v1_users_router

__all__ = [
    "v1_authorization_router",
    "v1_registration_router",
    "v1_users_router",
]
