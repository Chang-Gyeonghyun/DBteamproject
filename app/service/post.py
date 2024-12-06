import asyncio
import os
from typing import List
import aiofiles
from fastapi import Depends, HTTPException, UploadFile
from app.entity.models import Post
from app.entity.repository.repository import RepositoryFactory
from app.schemas.post.request import PostCreateRequest, PostUpdateRequest, PostFilterRequest
from app.schemas.post.response import AttachmentResponse, CommentResponse, ListPostsResponse, PostWithDetailsResponse
from app.utils.exceptions import CustomException, ExceptionEnum

class PostService:
    def __init__(self, repository_factory: RepositoryFactory = Depends()):
        self.post_repo = repository_factory.get_post_repository()
        self.keyword_repo = repository_factory.get_keyword_repository()
        self.attach_repo = repository_factory.get_attachment_repository()

    async def create_post(self, post_data: PostCreateRequest, files: List[UploadFile]):
        post: Post = await self.post_repo.create_post(post_data)
        if post_data.keywords:
            await self.keyword_repo.create_keyword(post.postID, post_data.keywords)
        if files:
            await asyncio.gather(
                self.save_files(files),                     
                self.attach_repo.create_attachment(post.postID, files) 
            )
        return

    async def get_post(self, post_id: int) -> PostWithDetailsResponse:
        post = await self.post_repo.get_post_detail_by_id(post_id)
        if not post:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        
        response = PostWithDetailsResponse(
            PostID=post.postID,
            Title=post.title,
            Content=post.content,
            Count_likes=post.count_likes,
            nickname=post.user.nickname,
            Create_at=post.create_at,
            Update_at=post.update_at,
            keyword=[kw.name for kw in post.keywords],
            attachment=[AttachmentResponse.from_orm(att) for att in post.attachments],
            comments=[CommentResponse.from_orm(comment) for comment in post.comments]
        )
        return response

    async def update_post(self, post_id: int, update_data: PostUpdateRequest, files: List[UploadFile]) -> PostWithDetailsResponse:
        post = await self.post_repo.get_post_by_id(post_id)
        if not post:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        
        post = await self.post_repo.update_post(post, update_data)
        if update_data.keywords:
            await self.keyword_repo.create_keyword(post.postID, update_data.keywords)
        if files:
            await asyncio.gather(
                self.save_files(files),                     
                self.attach_repo.create_attachment(post.postID, files) 
            )
        return
        
        return PostWithDetailsResponse.from_orm(post)

    async def delete_post(self, post_id: int) -> None:
        success = await self.post_repo.delete_post(post_id)
        if not success:
            raise HTTPException(status_code=404, detail="Post not found")

    async def filter_posts(self, filter_data: PostFilterRequest) -> ListPostsResponse:
        posts, total = await self.post_repo.filter_posts(filter_data)
        return ListPostsResponse(
            posts=[PostWithDetailsResponse.from_orm(post) for post in posts],
            page=filter_data.page,
            limit=filter_data.limit,
            total=total,
        )

    async def get_user_posts_by_category(self, user_id: str, category: str, page: int, limit: int) -> ListPostsResponse:
        posts, total = await self.post_repo.get_user_posts_by_category(user_id, category, page, limit)
        return ListPostsResponse(
            posts=[PostWithDetailsResponse.from_orm(post) for post in posts],
            page=page,
            limit=limit,
            total=total,
        )

    async def save_files(self, files: List[UploadFile]) -> List[str]:
        upload_dir = "./uploads/attachments"
        for file in files:
            file_path = os.path.join(upload_dir, file.filename)
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(await file.read())  
        return
