from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from fastapi import Depends, HTTPException
from app.database import get_database
from app.entity.models import Like, Post


class LikeRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session

    async def like_post(self, user_id: str, post_id: int):
        like = Like(userID=user_id, postID=post_id)
        self.session.add(like)
        await self.session.commit()
        return

    async def unlike_post(self, user_id: str, post_id: int):
        stmt = delete(Like).where(Like.userID == user_id, Like.postID == post_id)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Like not found")
        await self.session.commit()
