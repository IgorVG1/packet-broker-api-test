from pydantic import BaseModel, Field

from config import settings


class UserSchema(BaseModel):
    """
    Описание структуры pydantic-model UserSchema.
    Attributes:
        id: int
        username: str
        is_active: bool
        is_staff: bool
        is_specformat: bool
    """
    id: int
    username: str
    is_active: bool
    is_staff: bool
    is_specformat: bool


class LoginRequestSchema(BaseModel):
    """
    Описание структуры запроса на аутентификацию.
    Attributes:
        username: str
        password: str
    """
    username: str   = Field(default=settings.user_data.username)
    password: str   = Field(default=settings.user_data.password)


class LoginResponseSchema(BaseModel):
    """
    Описание структуры ответа на аутентификацию.
    Attributes:
        access: str
        refresh: str
        user: UserSchema
    """
    access: str
    refresh: str
    user: UserSchema


class RefreshRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление access_token.
    Attributes:
        refresh_token: str
    """
    refresh_token: str


class RefreshResponseSchema(BaseModel):
    """
    Описание структуры ответа на обновление access_token.
    Attributes:
        access: str
        refresh: str
    """
    access: str
    refresh: str