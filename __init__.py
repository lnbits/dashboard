import asyncio

from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .crud import db
from .tasks import wait_for_paid_invoices
from .views import publicdash_generic_router
from .views_api import publicdash_api_router

publicdash_ext: APIRouter = APIRouter(
    prefix="/publicdash", tags=["PublicDash"]
)
publicdash_ext.include_router(publicdash_generic_router)
publicdash_ext.include_router(publicdash_api_router)


publicdash_static_files = [
    {
        "path": "/publicdash/static",
        "name": "publicdash_static",
    }
]

scheduled_tasks: list[asyncio.Task] = []


def publicdash_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def publicdash_start():
    task = create_permanent_unique_task("ext_publicdash", wait_for_paid_invoices)
    scheduled_tasks.append(task)


__all__ = [
    "db",
    "publicdash_ext",
    "publicdash_start",
    "publicdash_static_files",
    "publicdash_stop",
]