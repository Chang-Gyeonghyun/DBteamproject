from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class AttachmentResponse(BaseModel):
    attachmentID: int
    fileName: str
    
    class Config:
        from_attributes = True

class CommentResponse(BaseModel):
    commentID: int
    parentcommentID: Optional[int]
    content: str
    userID: str
    nickname: str
    create_at: datetime
    replies: List["CommentResponse"] = []

class PostWithDetailsResponse(BaseModel):
    PostID: int
    Title: str
    Content: str
    Count_likes: int
    userID: str
    nickname: str
    Create_at: datetime
    Update_at: datetime
    keyword: Optional[List[str]] = None
    attachment: Optional[List[AttachmentResponse]] = None
    comments: Optional[List[CommentResponse]] = None

class PostResponse(BaseModel):
    postID: int
    title: str
    count_likes: int
    userID: str
    nickname: str
    create_at: datetime

class ListPostsResponse(BaseModel):
    posts: List[PostResponse]
    page: int
    limit: int
    total: int

    class Config:
        from_attributes = True
