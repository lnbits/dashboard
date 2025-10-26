import asyncio

from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .crud import db
from .tasks import wait_for_paid_invoices
from .views import dashboard_generic_router
from .views_api import dashboard_api_router

dashboard_ext: APIRouter = APIRouter(
    prefix="/dashboard", tags=["Dashboard"]
)
dashboard_ext.include_router(dashboard_generic_router)
dashboard_ext.include_router(dashboard_api_router)


dashboard_static_files = [
    {
        "path": "/dashboard/static",
        "name": "dashboard_static",
    }
]

scheduled_tasks: list[asyncio.Task] = []


def dashboard_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def dashboard_start():
    task = create_permanent_unique_task("ext_dashboard", wait_for_paid_invoices)
    scheduled_tasks.append(task)


__all__ = [
    "db",
    "dashboard_ext",
    "dashboard_start",
    "dashboard_static_files",
    "dashboard_stop",
]