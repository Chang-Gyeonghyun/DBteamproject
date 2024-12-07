from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.database import get_database
from app.entity.models import Keyword
from app.schemas.post.request import PostCreateRequest

class KeywordRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session
    
    async def create_keyword(self, post_id: int, post_data: PostCreateRequest):
        for keyword in post_data.keywords:
            if keyword:
                self.session.add(Keyword(postID=post_id, name=keyword))
        await self.session.commit()
        return 
    
    async def delete_keywords_by_post_id(self, post_id: int):
        await self.session.execute(
            delete(Keyword).where(Keyword.postID == post_id)
        )
        await self.session.commit()
        
