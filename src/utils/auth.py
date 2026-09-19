import jwt
from datetime import datetime, timedelta, UTC
from pwdlib import PasswordHash

from config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expires_at = datetime.now(UTC) + expires_delta
    else:
        expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expires
        )
    to_encode.update({"exp": expires_at})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]}
        )
    except jwt.InvalidTokenError:
        return None
    return payload.get("sub")
