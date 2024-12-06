from pydantic import BaseModel, Field
from typing import Optional, List


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
    keywords: Optional[List[str]] = None
    attachments: Optional[List[str]] = None

class PostFilterRequest(BaseModel):
    keyword: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
