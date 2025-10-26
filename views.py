# Description: Add your page endpoints here.

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer
from lnbits.settings import settings
from .crud import get_owner_data_by_id

publicdash_generic_router = APIRouter()


def publicdash_renderer():
    return template_renderer(["publicdash/templates"])


#######################################
##### ADD YOUR PAGE ENDPOINTS HERE ####
#######################################


# Backend admin page


@publicdash_generic_router.get("/", response_class=HTMLResponse)
async def index(req: Request, user: User = Depends(check_user_exists)):
    return publicdash_renderer().TemplateResponse(
        "publicdash/index.html", {"request": req, "user": user.json()}
    )


# Frontend shareable page


@publicdash_generic_router.get("/{owner_data_id}")
async def owner_data_public_page(req: Request, owner_data_id: str):
    owner_data = await get_owner_data_by_id(owner_data_id)
    if not owner_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Owner Data does not exist.")

    public_page_name = getattr(owner_data, "", "")

    return publicdash_renderer().TemplateResponse(
        "publicdash/public_page.html",
        {
            "request": req,
            "owner_data_id": owner_data_id,
            "public_page_name": public_page_name,
        },
    )



@publicdash_generic_router.get("/manifest/{owner_data_id}.webmanifest")
async def manifest(owner_data_id: str):
    owner_data = await get_owner_data_by_id(owner_data_id)
    if not owner_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Owner Data does not exist.")

    return {
        "short_name": "Dashboard " + owner_data.name,
        "name": "Scrum " + owner_data.name,
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
        "start_url": "/publicdash/" + owner_data_id,
        "background_color": "#1F2234",
        "description": "Bitcoin Lightning Scrum",
        "display": "standalone",
        "scope": "/publicdash/" + owner_data_id,
        "theme_color": "#1F2234",
        "shortcuts": [
            {
                "name": "Scrum " + owner_data.name + " - " + settings.lnbits_site_title,
                "short_name": "Scrum " + owner_data.name,
                "url": "/scrum/" + owner_data_id,
            }
        ],
    }
