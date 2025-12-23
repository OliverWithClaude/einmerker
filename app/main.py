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


@app.get("/seed", response_class=PlainTextResponse)
async def seed(db: AsyncSession = Depends(get_db)):
    """Public endpoint listing all public bookmark URLs for YaCy crawling."""
    result = await db.execute(
        select(Bookmark).where(Bookmark.public == True).order_by(Bookmark.created_at.desc())
    )
    bookmarks = result.scalars().all()
    urls = [b.url for b in bookmarks]
    return "\n".join(urls)


@app.get("/seed.json", response_model=List[PublicBookmarkResponse])
async def seed_json(db: AsyncSession = Depends(get_db)):
    """Public endpoint listing all public bookmarks as JSON."""
    result = await db.execute(
        select(Bookmark).where(Bookmark.public == True).order_by(Bookmark.created_at.desc())
    )
    return result.scalars().all()
