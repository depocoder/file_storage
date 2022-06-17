"""User model."""
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from file_storage.db.models.base import Base


class User(Base):
    """User model."""

    __tablename__ = "user_model"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    username = Column(String(length=32))  # noqa: WPS432
    hashed_password = Column(String(length=64))  # noqa: WPS432
    password_salt = Column(String(length=64))  # noqa: WPS432
    first_name = Column(String(length=32))  # noqa: WPS432
    surname = Column(String(length=32))  # noqa: WPS432
    email = Column(String(length=64), index=True)  # noqa: WPS432
    is_superuser = Column(Boolean, default=False)
