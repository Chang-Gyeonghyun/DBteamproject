from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import Depends, HTTPException
from app.database import get_database
from app.entity.models import Follow, User


class FollowRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session

    async def follow_user(self, user_id: str, follow_id: str):
        user = await self.session.scalar(select(User).where(User.userID == follow_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        existing_follow = await self.session.scalar(
            select(Follow).where(Follow.userID == user_id, Follow.followID == follow_id)
        )
        if existing_follow:
            raise HTTPException(status_code=409, detail="Already following")

        follow = Follow(userID=user_id, followID=follow_id)
        self.session.add(follow)
        await self.session.commit()

    async def unfollow_user(self, user_id: str, follow_id: str):
        stmt = delete(Follow).where(Follow.userID == user_id, Follow.followID == follow_id)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Follow not found")
        await self.session.commit()
