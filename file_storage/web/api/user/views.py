"""User view."""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from file_storage.db.crud.user import UserCRUD
from file_storage.db.dependencies import get_db_session
from file_storage.db.models.user import User
from file_storage.web.api.user.schema import BaseUserInDbScheme, UserWithPasswordScheme

router = APIRouter()


@router.get("/", response_model=List[BaseUserInDbScheme])
async def get_users(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db_session),
) -> List[User]:
    """
    Retrieve all Users objects from database.

    :param limit: limit of user objects, defaults to 10.
    :param offset: offset of user objects, defaults to 0.
    :param db: db session.
    :return: list of user obbjects from database.
    """
    return await UserCRUD(db).get_all(limit=limit, offset=offset)


@router.post("/")
async def create_user(
    user_object: UserWithPasswordScheme,
    db: AsyncSession = Depends(get_db_session),
) -> BaseUserInDbScheme:
    """
    Create User model in database.

    :param user_object: new user model item.
    :param db: db session.
    """
    user = await UserCRUD(db).create(user_object)
    user.password = "*" * len(user.password)
    return user
