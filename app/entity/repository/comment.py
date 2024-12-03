from fastapi import Depends
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.database import get_database
from app.entity.models import Comment
from app.schemas.comment.request import CommentRequest

class CommentRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session
               
    async def create_comment(self, request: CommentRequest) -> Comment:
        new_comment = Comment(
            content=request.content,
            userID=request.userID,
            postID=request.postID,
            parentcommentID=request.parentCommentID,
            create_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)
        return new_comment
    
    async def delete_comment(self, comment: Comment):
        await self.session.delete(comment)
        await self.session.commit()
        return
    
    async def get_comment_by_id(self, comment_id: int):
        comment = await self.session.scalar(
            select(Comment).where(Comment.commentID == comment_id)
        )
        return comment