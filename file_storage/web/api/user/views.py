"""User view."""
import base64
import json
from typing import List

from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession

from file_storage.db.crud.user import UserCRUD
from file_storage.db.dependencies import get_db_session
from file_storage.db.models.user import User
from file_storage.web.api.user.schema import BaseUserInDbScheme, UserWithPasswordScheme
from file_storage.web.api.user.utils import verify_password
from file_storage.web.cryptography import sign_cookie

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


@router.post("/login", name="login")
async def process_login_page(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db_session),
) -> Response:
    user = await UserCRUD(db).get_by_username(username)
    if not user:
        return Response(
            json.dumps(
                {
                    "success": False,
                    "message": "Username is not registered.",
                },
            ),
            media_type="application/json",
        )
    if not verify_password(password, user.hashed_password, user.password_salt):
        return Response(
            json.dumps(
                {
                    "success": False,
                    "message": "Password is incorrect.",
                },
            ),
            media_type="application/json",
        )
    response = Response(
        json.dumps(
            {
                "success": True,
                "message": "Login success",
            },
        ),
        media_type="application/json",
    )
    base64_username = base64.b64encode(username.encode()).decode()
    hashed_cookie = sign_cookie(username)
    cookie_value = f"{base64_username}.{hashed_cookie}"
    response.set_cookie(key="username", value=cookie_value)
    return response
