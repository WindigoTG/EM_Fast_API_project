import bcrypt


def hash_password(password: str | bytes) -> bytes:
    if not isinstance(password, bytes):
        password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password: str | bytes, hashed: bytes) -> bool:
    if not isinstance(password, bytes):
        password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed)
