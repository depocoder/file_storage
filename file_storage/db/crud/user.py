"""User CRUD."""
import hashlib
import hmac
import secrets
from typing import Type, TypeVar

from file_storage.db.crud.base import CRUDBase
from file_storage.db.models.user import User
from file_storage.web.api.user.schema import (
    UserDeleteScheme,
    UserReadScheme,
    UserUpdateScheme,
    UserWithHashedPasswordScheme,
    UserWithPasswordScheme,
)

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
        hashed_password = (
            hmac.new(
                passwod_salt.encode(),
                msg=password.encode(),
                digestmod=hashlib.sha256,
            )
            .hexdigest()
            .upper()
        )
        serialized_user.update(
            {"hashed_password": hashed_password, "password_salt": passwod_salt},
        )
        user_with_hashed_password = UserWithHashedPasswordScheme(**serialized_user)
        db_user_obj = self.model(**user_with_hashed_password.dict())
        self.session.add(db_user_obj)
        await self.session.flush()
        return user_obj
