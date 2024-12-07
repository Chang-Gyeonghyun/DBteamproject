from typing import Optional
from pydantic import BaseModel

class CommentRequest(BaseModel):
    postID: int
    parentCommentID: Optional[int] = None
    content: str
    userID: str