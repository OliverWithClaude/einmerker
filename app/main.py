from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.config import get_settings
from app.core.database import init_db, get_db
from app.api import api_router
from app.models.bookmark import Bookmark
from app.schemas.bookmark import PublicBookmarkResponse

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    description="A bookmarking and notes application",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API routes
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.app_name}


INTERVAL_DESCRIPTIONS = {
    "daily": "These bookmarks point to frequently updated content like news sites and should be crawled daily.",
    "weekly": "These bookmarks point to regularly updated content and should be crawled weekly.",
    "monthly": "These bookmarks point to occasionally updated content and should be crawled monthly.",
    "once": "These bookmarks point to static content that only needs to be crawled once.",
}


@app.get("/seed", response_class=HTMLResponse)
async def seed_index(request: Request):
    """Index page for seed endpoints."""
    return templates.TemplateResponse("seed_index.html", {"request": request})


@app.get("/seed/{interval}", response_class=HTMLResponse)
async def seed_by_interval(request: Request, interval: str, db: AsyncSession = Depends(get_db)):
    """Public endpoint listing bookmark URLs for YaCy crawling by interval."""
    if interval not in INTERVAL_DESCRIPTIONS:
        return HTMLResponse(content="Invalid interval. Use: daily, weekly, monthly, or once", status_code=404)

    result = await db.execute(
        select(Bookmark).where(Bookmark.crawl_interval == interval).order_by(Bookmark.created_at.desc())
    )
    bookmarks = result.scalars().all()

    return templates.TemplateResponse("seed.html", {
        "request": request,
        "interval": interval,
        "description": INTERVAL_DESCRIPTIONS[interval],
        "bookmarks": bookmarks
    })
