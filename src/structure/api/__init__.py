__all__ = [
    'router',
]

from fastapi import APIRouter

from .v1.routers import v1_api_router

router = APIRouter()
router.include_router(
    v1_api_router,
    prefix="/v1/divisions",
    tags=["v1", "divisions"],
)
