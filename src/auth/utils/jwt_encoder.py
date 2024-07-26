from datetime import datetime, timedelta

import jwt

from src.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
    token_lifetime: int = settings.ACCESS_TOKEN_LIFETIME,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=token_lifetime)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
):
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return decoded
