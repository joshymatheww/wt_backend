from sqlalchemy import func, select

from .base import BaseRepository
from models.user import User
from schemas.token import UserCreate, UserResponse
from utils.auth import hash_password


class UserRepository(BaseRepository):
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        new_user = User(
            **user_data.model_dump(exclude={"password"}, exclude_none=True),
            password_hash=hash_password(user_data.password)
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def check_user_exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(
            select(User).where(func.lower(User.email) == email.lower()),
        )
        user = result.scalars().first()
        return bool(user)

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(func.lower(User.email) == email.lower()),
        )
        user = result.scalars().first()
        return user

    async def get_user_by_id(self, user_id: id) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id),
        )
        user = result.scalars().first()
        return user
