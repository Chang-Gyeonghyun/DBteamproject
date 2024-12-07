from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.database import get_database
from app.entity.models import Follow, Like, Post, User
from app.schemas.user.request import PaginationParams, UserSignUp, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session
               
    async def create_user_entity(self, user_form: UserSignUp) -> User:
        new_user = User(
            userID=user_form.userID,
            email=user_form.email,
            hashed_password=user_form.password,
            phone=user_form.phone,
            gender=user_form.gender,
            birth=user_form.birth,
            name=user_form.name,
            nickname=user_form.nickname,
            profile_image=user_form.profile_image,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    async def search_user_by_id(self, userID: str) -> User | None:
        user = await self.session.scalar(
            select(User).where(User.userID == userID)
        )
        return user
    
    async def update_user(self, user: User, update_request: UserUpdate):
        for field, value in update_request.dict(exclude_unset=True).items():
            setattr(user, field, value)
            
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_likes(self, user_id: str, page_param: PaginationParams = None):
        query = (
            select(Post)
            .join(Like, Post.postID == Like.postID)
            .join(User, Like.userID == User.userID)
            .where(Like.userID == user_id)
        )
        
        if page_param is not None:
            offset = (page_param.page - 1) * page_param.limit
            query = query.offset(offset).limit(page_param.limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_user_follower(self, user_id: str, page_param: PaginationParams = None):
        query = (
            select(User, Follow.follow_at)
            .join(Follow, Follow.userID == User.userID)
            .where(Follow.followID == user_id)  
        )
        if page_param is not None:
            offset = (page_param.page - 1) * page_param.limit
            query = query.offset(offset).limit(page_param.limit)
        
        result = await self.session.execute(query)
        return result.all()

        
    async def get_user_following(self, user_id: str, page_param: PaginationParams = None):
        query = (
            select(User, Follow.follow_at)
            .join(Follow, Follow.followID == User.userID)
            .where(Follow.userID == user_id)
        )
        if page_param is not None:
            offset = (page_param.page - 1) * page_param.limit
            query = query.offset(offset).limit(page_param.limit)
        
        result = await self.session.execute(query)
        return result.all()

    
    async def delete_user(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
        return