from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from src.middlewares.auth import auth
from src.models.user import User
from src.schemas.token import TokenRequest, TokenResponse, UserCreate, UserResponse
from src.services.user_services import UserService

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def genereate_user_token(
    request: TokenRequest, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await UserService(session=db).login(login_details=request)


@router.post(
    "/create-admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_admin(db: Annotated[AsyncSession, Depends(get_db)]):
    user_details = UserCreate(
        first_name=settings.admin_first_name,
        last_name=settings.admin_last_name,
        email=settings.admin_email,
        password=settings.admin_password,
    )

    return await UserService(session=db).signup(user_details=user_details)


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: Annotated[User, Depends(auth)]):
    return current_user
