"""User schema."""

from pydantic import BaseModel, EmailStr, Field


class UserBaseScheme(BaseModel):
    """Base User Scheme."""

    username: str = Field(min_length=4, max_length=32)  # noqa: WPS432
    first_name: str = Field(default="", max_length=32)  # noqa: WPS432
    surname: str = Field(default="", max_length=32)  # noqa: WPS432
    email: EmailStr
    is_superuser: bool = False


class UserUpdateScheme(UserBaseScheme):
    """It returned when accessing user models from the API."""

    id: int


class UserDeleteScheme(UserBaseScheme):
    """It returned when accessing user models from the API."""

    id: int


class BaseUserInDbScheme(UserBaseScheme):
    """Base model for show user from DB."""

    class Config:
        orm_mode = True


class UserReadScheme(BaseUserInDbScheme):
    """Scheme for reading user model."""


class UserWithPasswordScheme(BaseUserInDbScheme):
    """Scheme with password."""

    password: str = Field(min_length=8, max_length=64)  # noqa: WPS432


class UserWithHashedPasswordScheme(BaseUserInDbScheme):
    """Scheme with hashed password and salt, for creating new user."""

    hashed_password: str = Field(min_length=64, max_length=64)  # noqa: WPS432
    password_salt: str = Field(min_length=64, max_length=64)  # noqa: WPS432
