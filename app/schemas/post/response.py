# from pydantic import BaseModel
# from typing import List

# class PostResponse(BaseModel):
#     PostID: int
#     Title: str
#     Count_likes: int
#     Create_at: str

# class ListPostsResponse(BaseModel):
#     posts: List[PostResponse]
#     page: int
#     limit: int
#     total: int
    
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class KeywordResponse(BaseModel):
    keywordID: int
    name: str

    class Config:
        orm_mode = True


class AttachmentResponse(BaseModel):
    attachmentID: int
    fileName: str
    filePath: str

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    postID: int
    title: str

    class Config:
        orm_mode = True


class PostWithDetailsResponse(PostResponse):
    content: str
    create_at: datetime
    update_at: datetime
    keywords: List[KeywordResponse]
    attachments: List[AttachmentResponse]

    class Config:
        orm_mode = True


class ListPostsResponse(BaseModel):
    posts: List[PostResponse]
    page: int
    limit: int
    total: int

    class Config:
        orm_mode = True
