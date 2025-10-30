from fastapi import APIRouter

from .crud import db
from .views import dashboard_generic_router
from .views_api import dashboard_api_router

dashboard_ext: APIRouter = APIRouter(prefix="/dashboard", tags=["Dashboard"])
dashboard_ext.include_router(dashboard_generic_router)
dashboard_ext.include_router(dashboard_api_router)

dashboard_static_files = [
    {
        "path": "/dashboard/static",
        "name": "dashboard_static",
    }
]

__all__ = [
    "dashboard_ext",
    "dashboard_static_files",
    "db",
]
