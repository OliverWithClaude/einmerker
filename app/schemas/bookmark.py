from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


class BookmarkBase(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    tags: Optional[str] = None
    public: bool = True


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    public: Optional[bool] = None


class BookmarkResponse(BookmarkBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PublicBookmarkResponse(BaseModel):
    title: str
    url: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
