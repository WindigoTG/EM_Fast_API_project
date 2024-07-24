from jwt.exceptions import InvalidTokenError
from fastapi import (
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)

from src.auth.schemas.user import UserSchema
from src.auth.schemas.jwt_token import TokenSchema
from src.auth.utils import jwt_encoder, password_hasher
from src.auth.units_of_work.auth import AuthUnitOfWork


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/jwt/login/",
)


class AuthorizationService:
    @classmethod
    async def mint_token(
        cls,
        uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
        account: str = Form(),
        password: str = Form(),
    ) -> TokenSchema:
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid account or password",
        )
        async with uow:
            account = await (
                uow.repositories[
                    "account"
                ].get_by_query_one_with_related_secret_one_or_none(
                    account=account,
                )
            )
        if not account or not account.is_verified or not account.secret:
            raise unauthed_exc

        if not password_hasher.check_password(
                password=password,
                hashed=account.secret.hashed_password,
        ):
            raise unauthed_exc

        token_payload = {
            "sub": account.secret.user.id.hex
        }
        token = jwt_encoder.encode_jwt(token_payload)
        return TokenSchema(
            access_token=token,
            token_type="Bearer",
        )

    @classmethod
    def get_current_auth_user(
        cls,
        uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
        token: str = Depends(oauth2_scheme)
    ) -> UserSchema:
        unauth_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token",
        )

        try:
            payload = jwt_encoder.decode_jwt(token=token)
        except InvalidTokenError:
            raise unauth_error

        user_id = payload.get("sub")
        if not user_id:
            raise unauth_error

        user = uow.repositories["user"].get_by_query_one_or_none(id=user_id)
        if not user:
            raise unauth_error

        return UserSchema.model_validate(user)
