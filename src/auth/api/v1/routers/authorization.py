from fastapi import APIRouter, Depends

from src.auth.services.authorization import AuthorizationService
from src.auth.schemas.jwt_token import TokenSchema

router = APIRouter()


@router.post("/login", response_model=TokenSchema)
async def login(
    token: TokenSchema = Depends(AuthorizationService.mint_token)
) -> TokenSchema:
    return token
