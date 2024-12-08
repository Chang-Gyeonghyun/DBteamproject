from pydantic import BaseModel
from typing import Literal, Optional, List
from fastapi import Form, Query


class PostCreateRequest(BaseModel):
    title: str
    content: str
    user_id: str
    keywords: Optional[List[str]] = None
    attachments: Optional[List[str]] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        user_id: str = Form(...),
        keywords: Optional[List[str]] = Form(None),
        attachments: Optional[List[str]] = Form(None),
    ):
        return cls(
            title=title,
            content=content,
            user_id=user_id,
            keywords=keywords,
            attachments=attachments,
        )


class PostUpdateRequest(BaseModel):
    title: str
    content: str
    user_id: str
    keywords: Optional[List[str]] = []
    attachments: Optional[List[str]] = []

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        user_id: str = Form(...),
        keywords: Optional[List[str]] = Form([]),
        attachments: Optional[List[str]] = Form([]),
    ):
        return cls(
            title=title,
            content=content,
            user_id=user_id,
            keywords=keywords,
            attachments=attachments,
        )

class PaginatedRequest(BaseModel):
    page: int = Query(default=1, ge=1)
    limit: int = Query(default=10, ge=1, le=100)
    
class UserKeywordRequest(PaginatedRequest):
    userID: str
    keyword: str

class MainFilterSearch(PaginatedRequest):
    keyword: Optional[str] = Query(default=None)
    field: Optional[Literal["title", "content", "title+content", "username"]] = Query(default=None)
    page: int = Query(default=1, ge=1)
    limit: int = Query(default=10, ge=1, le=100)