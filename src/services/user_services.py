from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.token import TokenResponse, UserCreate, UserResponse
from src.utils.auth import create_access_token, verify_password


class UserService:
    def __init__(self, session: AsyncSession):
        self._user_repository = UserRepository(session=session)

    async def signup(self, user_details: UserCreate) -> UserResponse:
        user_exists = await self._user_repository.check_user_exists_by_email(
            email=user_details.email
        )
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin user already exists. Please login",
            )
        return await self._user_repository.create_user(user_data=user_details)

    async def login(self, login_details: UserCreate) -> TokenResponse:
        user = await self._user_repository.get_user_by_email(email=login_details.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        if not verify_password(
            password=login_details.password, hashed_password=user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        access_token = create_access_token(data={"sub": str(user.id)})

        return TokenResponse(access_token=access_token, token_type="bearer")

    async def get_user(self, user_id: int) -> User:
        user = await self._user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
