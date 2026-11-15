from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware

import core
from routers import sola_pages, static
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

# Reassemble the upstream 6.4 MB standalone HTML file from smaller tracked parts.
# This avoids connector upload-size limits while preserving its content.
def _assemble_large_html():
    target = Path("templates/tool/youtube/xerox.html")
    pieces = sorted(Path("templates/tool/youtube/xerox_parts").glob("part_*.txt"))
    if not target.exists() and len(pieces) == 21:
        with target.open("w", encoding="utf-8", newline="") as output:
            for piece in pieces:
                output.write(piece.read_text(encoding="utf-8"))


_assemble_large_html()

app = FastAPI(title="SOLA TUBE", lifespan=lifespan)

for router in [
    proxy.router, thumb.router, shorts.router, watch.router, channel.router,
    search.router, download.router, static.router, sola_pages.router,
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
