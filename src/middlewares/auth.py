from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from src.schemas.token import UserResponse
from src.services.user_services import UserService
from src.utils.auth import verify_token

security_scheme = HTTPBearer()

AUTH_PREFIX = "Bearer"


async def auth(
    session: Annotated[AsyncSession, Depends(get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
) -> UserResponse:
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )

    authorization = credentials.scheme

    if not authorization:
        raise auth_exception
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    token = credentials.credentials
    user_id = verify_token(token=token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authorization": "Bearer"},
        )

    try:
        user_id = int(user_id)
    except TypeError, ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authorization": "Bearer"},
        )
    user = await UserService(session=session).get_user(user_id=user_id)
    return user
