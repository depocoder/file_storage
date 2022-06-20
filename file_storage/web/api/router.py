"""Main router."""
from fastapi.routing import APIRouter

from file_storage.web.api import docs, echo, monitoring, user
from file_storage.web.api.server.views import router as server_router

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(server_router, tags=["auth"])
