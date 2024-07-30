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

from src.auth.models import User
from src.auth.schemas.user import UserSchema
from src.auth.schemas.jwt_token import TokenSchema
from src.auth.utils import jwt_encoder, password_hasher
from src.auth.utils.enums import TokenTypeEnum
from src.auth.units_of_work.auth import AuthUnitOfWork
from src.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/jwt/login/",
)


class AuthorizationService:
    INVALID_TOKEN_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
    UNAUTHENTICATED_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid account or password",
    )
    TOKEN_TYPE_FIELD = "type"

    @classmethod
    async def mint_token(
        cls,
        uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
        account: str = Form(alias="username", ),
        password: str = Form(),
    ) -> TokenSchema:

        async with uow:
            account = await (
                uow.repositories[
                    "account"
                ].get_by_query_one_with_related_secret_one_or_none(
                    account=account,
                )
            )
        if not account or not account.is_verified or not account.secret:
            raise cls.UNAUTHENTICATED_EXCEPTION

        if not password_hasher.check_password(
                password=password,
                hashed=account.secret.hashed_password,
        ):
            raise cls.UNAUTHENTICATED_EXCEPTION

        access_token = cls._create_access_token(
            account.secret.user,
            TokenTypeEnum.ACCESS,
        )
        refresh_token = cls._create_access_token(
            account.secret.user,
            TokenTypeEnum.REFRESH,
        )

        return TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @classmethod
    async def refresh_token(
            cls,
            uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
            token: str = Depends(oauth2_scheme)
    ) -> TokenSchema:
        user = await cls._get_user_from_token(
            token,
            TokenTypeEnum.REFRESH,
            uow,
        )
        token = cls._create_access_token(user, TokenTypeEnum.ACCESS)

        return TokenSchema(
            access_token=token,
        )

    @classmethod
    async def get_current_auth_user(
        cls,
        uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
        token: str = Depends(oauth2_scheme)
    ) -> UserSchema:

        user = await AuthorizationService._get_user_from_token(
            token,
            TokenTypeEnum.ACCESS,
            uow,
        )

        return UserSchema.model_validate(user)

    @classmethod
    async def get_current_auth_admin(
        cls,
        uow: AuthUnitOfWork = Depends(AuthUnitOfWork),
        token: str = Depends(oauth2_scheme),
    ):
        current_user = await AuthorizationService.get_current_auth_user(
            uow,
            token,
        )

        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a company admin",
            )

        return current_user

    @classmethod
    def _get_token_payload(cls, token: str):
        try:
            payload = jwt_encoder.decode_jwt(token=token)
        except InvalidTokenError:
            raise cls.INVALID_TOKEN_EXCEPTION
        return payload

    @classmethod
    async def _get_user_from_token(
        cls,
        token: str,
        token_type: TokenTypeEnum,
        uow: AuthUnitOfWork,
    ) -> User:
        payload = cls._get_token_payload(token)
        cls._validate_token_type(payload, token_type)
        user_id = payload.get("sub")
        if not user_id:
            raise cls.INVALID_TOKEN_EXCEPTION
        async with uow:
            user = await uow.repositories["user"].get_by_query_one_or_none(
                id=user_id,
            )
            if not user:
                raise cls.INVALID_TOKEN_EXCEPTION

        return user

    @classmethod
    def _validate_token_type(
        cls,
        payload: dict,
        token_type: TokenTypeEnum,
    ) -> bool:
        current_token_type = payload.get(cls.TOKEN_TYPE_FIELD)
        if current_token_type == token_type.value:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token type {curr}, expected {exp}".format(
                curr=repr(current_token_type),
                exp=repr(token_type.value)
            ),
        )

    @classmethod
    def _create_access_token(cls, user: User, token_type: TokenTypeEnum):
        token_payload = {
            "sub": user.id.hex,
            cls.TOKEN_TYPE_FIELD: token_type.value
        }

        if token_type == TokenTypeEnum.ACCESS:
            lifetime = settings.ACCESS_TOKEN_LIFETIME
        else:
            lifetime = settings.REFRESH_TOKEN_LIFETIME * 60 * 24

        return jwt_encoder.encode_jwt(token_payload, token_lifetime=lifetime)
