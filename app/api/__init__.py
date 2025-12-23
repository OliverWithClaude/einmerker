from fastapi import APIRouter
from app.api import auth, bookmarks, notes

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(bookmarks.router)
api_router.include_router(notes.router)
