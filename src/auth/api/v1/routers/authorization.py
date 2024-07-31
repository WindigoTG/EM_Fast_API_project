from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.auth.services.authorization import AuthorizationService
from src.auth.schemas.jwt_token import TokenSchema


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post("/login", response_model=TokenSchema)
async def login(
    token: TokenSchema = Depends(AuthorizationService.mint_token)
) -> TokenSchema:

    return token


@router.post(
    "/refresh",
    response_model=TokenSchema,
    response_model_exclude_none=True,
)
async def refresh_token(
    token: TokenSchema = Depends(AuthorizationService.refresh_token)
):
    return token
