from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class AttachmentResponse(BaseModel):
    attachmentID: int
    fileName: str
    
    model_config = ConfigDict(from_attributes=True)

class CommentResponse(BaseModel):
    CommentID: int
    ParentCommentID: Optional[int]
    Content: str
    UserID: str
    create_at: datetime
    Replies: List["CommentResponse"] = []

    model_config = ConfigDict(from_attributes=True)

class PostWithDetailsResponse(BaseModel):
    PostID: int
    Title: str
    Content: str
    Count_likes: int
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
    nickname: str
    create_at: datetime

class ListPostsResponse(BaseModel):
    posts: List[PostResponse]
    page: int
    limit: int
    total: int

    class Config:
        orm_mode = True
