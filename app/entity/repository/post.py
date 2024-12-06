from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload, joinedload
from typing import Optional, List, Tuple
from app.database import get_database
from app.entity.models import Comment, Post, Keyword, PostKeyword, Attachment
from app.schemas.post.request import PostCreateRequest, PostUpdateRequest, PostFilterRequest


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
    
    async def get_post_by_id(self, post_id: int) -> Optional[Post]:
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

    async def update_post(self, post: Post, update_data: PostUpdateRequest) -> Optional[Post]:
        for field, value in update_data.dict(exclude_unset=True).items():
            if hasattr(post, field):
                setattr(post, field, value)
                
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

        if update_data.keywords is not None:
            await self.session.execute(delete(PostKeyword).where(PostKeyword.postID == post_id))
            for keyword in update_data.keywords:
                db_keyword = await self.session.scalar(select(Keyword).where(Keyword.name == keyword))
                if not db_keyword:
                    db_keyword = Keyword(name=keyword)
                    self.session.add(db_keyword)
                    await self.session.flush()
                self.session.add(PostKeyword(postID=post_id, keywordID=db_keyword.keywordID))

        if update_data.attachments is not None:
            await self.session.execute(delete(Attachment).where(Attachment.postID == post_id))
            for attachment in update_data.attachments:
                self.session.add(Attachment(
                    postID=post_id,
                    fileName=attachment,
                    filePath=f"/uploads/{attachment}",
                ))

        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def delete_post(self, post_id: int) -> bool:
        post = await self.get_post_by_id(post_id)
        if not post:
            return False
        await self.session.delete(post)
        await self.session.commit()
        return True

    async def filter_posts(self, filter_data: PostFilterRequest) -> Tuple[List[Post], int]:
        offset = (filter_data.page - 1) * filter_data.limit

        stmt = select(Post).offset(offset).limit(filter_data.limit).options(selectinload(Post.keywords))
        if filter_data.keyword:
            stmt = stmt.join(PostKeyword).join(Keyword).where(Keyword.name == filter_data.keyword)

        result = await self.session.execute(stmt)
        posts = result.scalars().all()

        count_stmt = select(func.count()).select_from(Post)
        if filter_data.keyword:
            count_stmt = count_stmt.join(PostKeyword).join(Keyword).where(Keyword.name == filter_data.keyword)

        total_result = await self.session.execute(count_stmt)
        total_count = total_result.scalar()

        return posts, total_count

    async def get_user_posts_by_category(self, user_id: str, category: str, page: int, limit: int) -> Tuple[List[Post], int]:
        offset = (page - 1) * limit

        stmt = (
            select(Post)
            .where(Post.userID == user_id, Post.categoryname == category)
            .offset(offset)
            .limit(limit)
            .options(selectinload(Post.keywords))
        )
        result = await self.session.execute(stmt)
        posts = result.scalars().all()

        count_stmt = select(func.count()).where(Post.userID == user_id, Post.categoryname == category)
        total_result = await self.session.execute(count_stmt)
        total_count = total_result.scalar()

        return posts, total_count
