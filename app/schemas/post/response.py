from pydantic import BaseModel
from typing import List

class PostResponse(BaseModel):
    PostID: int
    Title: str
    Count_likes: int
    Create_at: str

class ListPostsResponse(BaseModel):
    posts: List[PostResponse]
    page: int
    limit: int
    total: int