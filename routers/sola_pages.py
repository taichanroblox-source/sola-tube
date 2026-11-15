"""SOLA TUBE public page routes. No shared-password gate from the source project."""
import json

from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from core import templates

router = APIRouter()

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"active": "home"})

@router.get("/trending")
async def trending(request: Request):
    return templates.TemplateResponse(request, "trending.html", {"active": "trending"})

@router.get("/dl")
async def downloader(request: Request):
    return templates.TemplateResponse(request, "dl.html", {"active": "dl"})

@router.get("/watch")
async def watch(request: Request):
    return templates.TemplateResponse(request, "watch.html")

@router.get("/shorts/{video_id}")
async def shorts(request: Request, video_id: str):
    from routers.videos.watch import _EDU_PARAMS_CACHE
    cached = _EDU_PARAMS_CACHE.get("data")
    edu_params_json = json.dumps(cached["json"] if cached else [])
    return templates.TemplateResponse(request, "shorts.html", {"edu_params_json": edu_params_json})

@router.get("/search")
async def search(request: Request):
    return templates.TemplateResponse(request, "search.html")

@router.get("/channel")
async def channel(request: Request):
    return templates.TemplateResponse(request, "channel.html")

@router.get("/playlist")
async def playlist(request: Request):
    return templates.TemplateResponse(request, "playlist.html")

@router.get("/hashtag")
async def hashtag(request: Request):
    return templates.TemplateResponse(request, "hashtag.html")

@router.get("/mix")
async def mix_page(request: Request):
    return templates.TemplateResponse(request, "mix.html")

@router.get("/library")
async def library(request: Request):
    return templates.TemplateResponse(request, "library.html", {"active": "library"})

@router.get("/settings")
async def settings(request: Request):
    return templates.TemplateResponse(request, "settings.html", {"active": "settings"})

@router.get("/links")
async def links(request: Request):
    return templates.TemplateResponse(request, "links.html")

@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html", {"active": "about", "current_version": "SOLA 0.1", "is_first_visit": False})

@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse(request, "contact.html")

@router.get("/chat")
async def chat():
    return RedirectResponse("https://sola-portal.onrender.com/chat")

@router.get("/talk")
async def talk():
    return RedirectResponse("https://sola-portal.onrender.com/talk")
