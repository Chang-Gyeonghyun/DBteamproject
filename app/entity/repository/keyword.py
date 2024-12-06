from typing import List
from fastapi import Depends
from datetime import datetime
from sqlalchemy import select
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
            self.session.add(Keyword(postID=post_id, name=keyword))
        await self.session.flush()
        return 
        
