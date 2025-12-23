from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
from typing import Optional, List, Literal


CRAWL_INTERVALS = ["daily", "weekly", "monthly", "once", "never"]
CrawlInterval = Literal["daily", "weekly", "monthly", "once", "never"]


class BookmarkBase(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    tags: Optional[str] = None
    crawl_interval: CrawlInterval = "weekly"


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    crawl_interval: Optional[CrawlInterval] = None


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
