"""User CRUD."""
import logging
import secrets
from typing import Optional, Type, TypeVar

from sqlalchemy import select

from file_storage.db.crud.base import CRUDBase
from file_storage.db.models.user import User
from file_storage.web.api.cryptography import hash_password
from file_storage.web.api.user.schema import (
    UserDeleteScheme,
    UserReadScheme,
    UserUpdateScheme,
    UserWithHashedPasswordScheme,
    UserWithPasswordScheme,
)

logger = logging.getLogger(__name__)
ModelType = TypeVar("ModelType", bound=User)
PASSWORD_SALT_LEN = 32


class UserCRUD(
    CRUDBase[
        User,
        UserWithPasswordScheme,
        UserReadScheme,
        UserUpdateScheme,
        UserDeleteScheme,
    ],
):
    """Class for accessing User table."""

    @property
    def model(self) -> Type[User]:
        """Get user model."""
        return User

    async def create(
        self,
        user_obj: UserWithPasswordScheme,
    ) -> UserWithPasswordScheme:
        """Create model in DB."""
        serialized_user = user_obj.dict()
        password = serialized_user.pop("password")
        passwod_salt = secrets.token_hex(PASSWORD_SALT_LEN)
        hashed_password = hash_password(password, passwod_salt)
        serialized_user.update(
            {"hashed_password": hashed_password, "password_salt": passwod_salt},
        )
        user_with_hashed_password = UserWithHashedPasswordScheme(**serialized_user)
        db_user_obj = self.model(**user_with_hashed_password.dict())
        self.session.add(db_user_obj)
        await self.session.flush()
        return user_obj

    async def get_by_username(
        self,
        username: str,
    ) -> Optional[ModelType]:
        """Get user by username."""
        query = select(self.model).where(self.model.username == username)
        logger.info(
            "A query has been sent to db to get an user",
            extra={"username": username},
        )
        if (query_result := await self.session.execute(query)) is None:
            logger.info(
                "There is no user for the username",
                extra={"username": username},
            )
            return None
        logger.info(
            "Succesfully got an user",
            extra={"username": username},
        )
        return query_result.scalars().first()
