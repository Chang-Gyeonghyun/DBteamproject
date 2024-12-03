from pydantic import BaseModel

class CommentRequest(BaseModel):
    postID: int
    parentCommentID: int
    content: str
    userID: str