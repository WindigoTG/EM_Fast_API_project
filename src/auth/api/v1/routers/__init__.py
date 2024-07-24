from .authorization import router as v1_authorization_router
from .registration import router as v1_registration_router

__all__ = [
    "v1_authorization_router",
    "v1_registration_router",
]
