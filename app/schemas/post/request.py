from pydantic import BaseModel
from typing import Optional, List
from fastapi import Query


class PostCreateRequest(BaseModel):
    title: str
    content: str
    user_id: str
    keywords: Optional[List[str]] = None
    attachments: Optional[List[str]] = None


class PostUpdateRequest(BaseModel):
    title: str
    content: str
    user_id: str
    keywords: Optional[List[str]] = []
    attachments: Optional[List[str]] = []

class PaginatedRequest(BaseModel):
    page: int = Query(default=1, ge=1)
    limit: int = Query(default=10, ge=1, le=100)
    
class UserKeywordRequest(PaginatedRequest):
    userID: str
    keyword: str
