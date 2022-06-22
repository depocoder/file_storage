"""Api router."""
from fastapi.routing import APIRouter

from file_storage.web.api import docs, echo, monitoring, user

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
