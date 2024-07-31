__all__ = [
    'router',
]

from fastapi import APIRouter

from .v1.routers import v1_division_router, v1_position_router

router = APIRouter()
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
