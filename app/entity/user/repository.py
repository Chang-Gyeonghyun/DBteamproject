from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_database
from app.schemas.user.request import UserSignUp, UserUpdate
from app.entity.user.document import User

class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session
               
    async def create_user_entity(self, user_form: UserSignUp) -> User:
        new_user = User(
            userID=user_form.userID,
            email=user_form.email,
            hashed_password=user_form.password,
            phone=user_form.phone,
            gende=user_form.gender,
            birth=user_form.birth,
            name=user_form.name,
            nickname=user_form.nickname,
            profile_image=user_form.profileImage,
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
    
    async def delete_user(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
        return