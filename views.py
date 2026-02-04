from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer
from lnbits.settings import settings

from .crud import get_client_data_paginated, get_owner_data_by_id

dashboard_generic_router = APIRouter()


def dashboard_renderer():
    return template_renderer(["dashboard/templates"])


@dashboard_generic_router.get("/", response_class=HTMLResponse)
async def index(req: Request, user: User = Depends(check_user_exists)):
    return dashboard_renderer().TemplateResponse("dashboard/index.html", {"request": req, "user": user.json()})


@dashboard_generic_router.get("/{owner_data_id}")
async def owner_data_public_page(req: Request, owner_data_id: str):
    owner_data = await get_owner_data_by_id(owner_data_id)
    if not owner_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Owner Data does not exist.")

    public_page_name = getattr(owner_data, "", "")
    links = await get_client_data_paginated([owner_data_id])
    if not links.data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Client Data does not exist.")

    links_list = [link.dict(exclude={"created_at", "updated_at"}) for link in links.data]
    return dashboard_renderer().TemplateResponse(
        "dashboard/public_page.html",
        {
            "request": req,
            "owner_data_id": owner_data_id,
            "public_page_name": public_page_name,
            "links": links_list,
            "web_manifest": f"/dashboard/manifest/{owner_data_id}.webmanifest",
        },
    )


@dashboard_generic_router.get("/manifest/{owner_data_id}.webmanifest")
async def manifest(owner_data_id: str):
    owner_data = await get_owner_data_by_id(owner_data_id)
    if not owner_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Owner Data does not exist.")

    return {
        "short_name": "Dashboard " + owner_data.name,
        "name": "Dashboard " + owner_data.name,
        "icons": [
            {
                "src": (
                    settings.lnbits_custom_logo
                    if settings.lnbits_custom_logo
                    else "https://cdn.jsdelivr.net/gh/lnbits/lnbits@0.3.0/docs/logos/lnbits.png"
                ),
                "type": "image/png",
                "sizes": "900x900",
            }
        ],
        "start_url": "/dashboard/" + owner_data_id,
        "background_color": "#1F2234",
        "description": "LNbits dashboard",
        "display": "standalone",
        "scope": "/dashboard/" + owner_data_id,
        "theme_color": "#2C1F34",
        "shortcuts": [
            {
                "name": "Dashboard " + owner_data.name + " - " + settings.lnbits_site_title,
                "short_name": "Dashboard " + owner_data.name,
                "description": "Dashboard " + owner_data.name,
                "url": "/dashboard/" + owner_data_id,
            }
        ],
    }
