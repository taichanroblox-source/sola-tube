from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware

import core
from routers import pages, static
from routers.proxy import proxy, thumb
from routers.videos import watch, channel, shorts, search, download
from routers.tool import youtube as tool_youtube
from routers.tool import game as tool_game
from routers.tool import programing as tool_programing
from routers.tool import proxy as tool_proxy

@asynccontextmanager
async def lifespan(app: FastAPI):
    core.http_client = httpx.AsyncClient(
        timeout=core._CLIENT_TIMEOUT,
        limits=core._CLIENT_LIMITS,
        follow_redirects=True,
    )
    yield
    await core.http_client.aclose()

app = FastAPI(title="SOLA TUBE", lifespan=lifespan)

for router in [
    proxy.router, thumb.router, shorts.router, watch.router, channel.router,
    search.router, download.router, static.router, pages.router,
    tool_youtube.router, tool_game.router, tool_programing.router, tool_proxy.router
]:
    app.include_router(router)

app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.mount("/photo", StaticFiles(directory="photo"), name="photo")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "sola-tube"}

class StaticCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=86400"
        return response

app.add_middleware(StaticCacheMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=500)
