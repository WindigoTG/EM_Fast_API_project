__all__ = [
    'router',
]

from fastapi import APIRouter

from .v1.routers import (
    v1_authorization_router,
    v1_division_router,
    v1_position_router,
    v1_registration_router,
    v1_users_router,
)


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
router.include_router(
    v1_users_router,
    prefix="/v1/users",
    tags=["v1", "users"],
)
router.include_router(
    v1_division_router,
    prefix="/v1/divisions",
    tags=["v1", "divisions", "structure"],
)
router.include_router(
    v1_position_router,
    prefix="/v1/positions",
    tags=["v1", "positions", "structure"],
)
