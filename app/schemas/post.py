from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class PostCreateRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class PostResponse(BaseModel):
    id: str
    user_id: str
    username: str
    content: str
    likes_count: int
    is_liked_by_me: bool
    created_at: datetime

class PostListResponse(BaseModel):
    posts: List[PostResponse]
    next_cursor: Optional[str] = None
    has_more: bool
