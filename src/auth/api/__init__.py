__all__ = [
    'router',
]

from fastapi import APIRouter

from .v1.routers import v1_authorization_router, v1_registration_router

router = APIRouter()
router.include_router(
    v1_authorization_router,
    prefix="/v1/auth/jwt",
    tags=["v1", "auth"],
)
router.include_router(
    v1_registration_router,
    prefix="/v1/auth",
    tags=["v1", "auth"],
)
