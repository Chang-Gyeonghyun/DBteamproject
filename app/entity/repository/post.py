from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func, update
from sqlalchemy.orm import selectinload, joinedload
from typing import Optional, List, Tuple
from app.database import get_database
from app.entity.models import Comment, Post, Keyword, Attachment
from app.schemas.post.request import PaginatedRequest, PostCreateRequest, PostUpdateRequest, UserKeywordRequest


class PostRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session

    async def create_post(self, post_data: PostCreateRequest) -> Post:
        new_post = Post(
            title=post_data.title,
            content=post_data.content,
            userID=post_data.user_id,
        )
        self.session.add(new_post)
        await self.session.flush()
        return new_post

    async def get_post_detail_by_id(self, post_id: int) -> Optional[Post]:
        query = (
            select(Post)
            .options(
                joinedload(Post.user),  
                joinedload(Post.comments).joinedload(Comment.replies),  
                joinedload(Post.likes),  
                joinedload(Post.attachments),  
                joinedload(Post.keywords), 
            )
            .where(Post.postID == post_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_post_by_id(self, post_id: int):
        post = await self.session.scalar(
            select(Post).where(Post.postID == post_id)
        )
        return post
    
    async def update_likes(self, post_id: int, unlike: bool = False):
        stmt = (
            update(Post)
            .where(Post.postID == post_id)
            .values(count_likes=Post.count_likes + (-1 if unlike else 1))
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return
    
    async def update_post(self, post_id: str, update_data: dict) -> Post:
        await self.session.execute(
            update(Post)
            .where(Post.postID == post_id)
            .values(**update_data)
        )
        await self.session.commit()
        return 

    async def delete_post(self, post: Post) -> bool:
        await self.session.delete(post)
        await self.session.commit()
        return

    async def treding_posts(self, filter_data: PaginatedRequest) -> Tuple[List[Post], int]:
        offset = (filter_data.page - 1) * filter_data.limit
        stmt = (
            select(Post)
            .options(joinedload(Post.user))
            .order_by(Post.count_likes.desc())
            .offset(offset)
            .limit(filter_data.limit)
        )
        result = await self.session.execute(stmt)
        posts = result.scalars().all()

        count_stmt = select(func.count()).select_from(Post)
        total_result = await self.session.execute(count_stmt)
        total_count = total_result.scalar()

        return posts, total_count

    async def get_user_posts_by_category(self, request: UserKeywordRequest) -> Tuple[List[Post], int]:
        offset = (request.page - 1) * request.limit

        stmt = (
            select(Post)
            .join(Post.keywords)  
            .options(joinedload(Post.user))  
            .where(Keyword.name == request.keyword) 
            .order_by(Post.count_likes.desc())
            .offset(offset)
            .limit(request.limit)
        )

        # 데이터 가져오기
        result = await self.session.execute(stmt)
        posts = result.scalars().all()

        # 총 개수 계산
        count_stmt = (
            select(func.count(Post.postID))  
            .join(Post.keywords)
            .where(Keyword.name == request.keyword)
        )
        total_result = await self.session.execute(count_stmt)
        total_count = total_result.scalar()

        return posts, total_count



