from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import Depends, HTTPException
from app.database import get_database
from app.entity.models import Follow, User


class FollowRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session

    async def follow_user(self, user_id: str, follow_id: str):
        follow = Follow(userID=user_id, followID=follow_id)
        self.session.add(follow)
        await self.session.commit()

    async def unfollow_user(self, user_id: str, follow_id: str):
        stmt = delete(Follow).where(Follow.userID == user_id, Follow.followID == follow_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return

    async def get_follow(self, user_id: str, follow_id: str):
        follow = await self.session.scalar(
            select(Follow).where(Follow.userID == user_id, Follow.followID == follow_id)
        )
        
        return follow
