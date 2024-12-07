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
        if post_data.keywords:
            # 키워드가 리스트 안에 쉼표로 연결된 문자열일 경우 처리
            keywords = []
            for item in post_data.keywords:
                if isinstance(item, str):
                    # 쉼표로 분리 후 공백 제거
                    keywords.extend([k.strip() for k in item.split(",")])

            # 중복 제거 및 빈 문자열 필터링
            keywords = list(filter(None, set(keywords)))

            for keyword in keywords:
                self.session.add(Keyword(postID=post_id, name=keyword))

        await self.session.commit()
        return


    async def delete_keywords_by_post_id(self, post_id: int):
        await self.session.execute(
            delete(Keyword).where(Keyword.postID == post_id)
        )
        await self.session.commit()
        
