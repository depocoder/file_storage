"""Fast api main app."""
import base64
import hmac
import json
import pathlib
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Form
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from file_storage.db.crud.user import UserCRUD
from file_storage.db.dependencies import get_db_session
from file_storage.settings import settings
from file_storage.web.api.cryptography import hash_password, sign_cookie

router = APIRouter()


def get_username_from_cookie(username_cookie: str) -> Optional[str]:
    """Get username from signed cookie."""
    username, sign = username_cookie.split(".")
    username = base64.b64decode(username.encode()).decode()
    valid_sing = sign_cookie(username)
    if hmac.compare_digest(valid_sing, sign):
        return username


def verify_password(
    password: str,
    stored_hashed_password: str,
    password_salt: str,
) -> bool:
    """Verify paasword for user."""
    hashed_password = hash_password(password, password_salt)
    return stored_hashed_password == hashed_password


@router.get("/")
async def index_page(
    username: Optional[str] = Cookie(default=None),
    db: AsyncSession = Depends(get_db_session),
) -> Response:
    template_path = pathlib.Path(
        settings.template_dir,
        "index.html",
    )
    with open(template_path) as index_file:
        html = index_file.read()
        response = Response(html, media_type="text/html")
    if not username:
        return response

    valid_username = get_username_from_cookie(username)
    if not valid_username:
        response.delete_cookie("username")
        return response

    user = await UserCRUD(db).get_by_username(valid_username)
    if user:
        return Response(
            f"You have already logged in your account. Your login {valid_username}",
            media_type="text/html",
        )
    response.delete_cookie("username")
    return response


@router.post("/login")
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
