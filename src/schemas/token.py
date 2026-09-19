from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TokenRequest(BaseModel):
    email: EmailStr = Field(min_length=1)
    password: str = Field(min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str | None = Field(min_length=1, default=None, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
