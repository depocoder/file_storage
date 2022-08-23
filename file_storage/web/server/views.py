"""Fast api main views."""
import base64
import hmac
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Request
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from file_storage.db.crud.user import UserCRUD
from file_storage.db.dependencies import get_db_session
from file_storage.settings import settings
from file_storage.web.cryptography import sign_cookie

templates = Jinja2Templates(directory=settings.template_dir)

router = APIRouter()


def get_username_from_cookie(username_cookie: str) -> Optional[str]:
    """Get username from signed cookie."""
    username, sign = username_cookie.split(".")
    username = base64.b64decode(username.encode()).decode()
    valid_sing = sign_cookie(username)
    if hmac.compare_digest(valid_sing, sign):
        return username


@router.get("/")
async def index_page(
    request: Request,
    username: Optional[str] = Cookie(default=None),
    db: AsyncSession = Depends(get_db_session),
) -> Response:
    response = templates.TemplateResponse("index.html", {"request": request})
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
