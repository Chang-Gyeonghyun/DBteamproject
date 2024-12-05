from typing import List
from fastapi import HTTPException
from app.entity.repository.post import PostRepository
from app.schemas.post.request import PostCreateRequest, PostUpdateRequest, PostFilterRequest
from app.schemas.post.response import PostWithDetailsResponse, ListPostsResponse

class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def create_post(self, post_data: PostCreateRequest) -> PostWithDetailsResponse:
        post = await self.repository.create_post(post_data)
        return PostWithDetailsResponse.from_orm(post)

    async def get_post(self, post_id: int) -> PostWithDetailsResponse:
        post = await self.repository.get_post_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return PostWithDetailsResponse.from_orm(post)

    async def update_post(self, post_id: int, update_data: PostUpdateRequest) -> PostWithDetailsResponse:
        post = await self.repository.update_post(post_id, update_data)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return PostWithDetailsResponse.from_orm(post)

    async def delete_post(self, post_id: int) -> None:
        success = await self.repository.delete_post(post_id)
        if not success:
            raise HTTPException(status_code=404, detail="Post not found")

    async def filter_posts(self, filter_data: PostFilterRequest) -> ListPostsResponse:
        posts, total = await self.repository.filter_posts(filter_data)
        return ListPostsResponse(
            posts=[PostWithDetailsResponse.from_orm(post) for post in posts],
            page=filter_data.page,
            limit=filter_data.limit,
            total=total,
        )

    async def get_user_posts_by_category(self, user_id: str, category: str, page: int, limit: int) -> ListPostsResponse:
        posts, total = await self.repository.get_user_posts_by_category(user_id, category, page, limit)
        return ListPostsResponse(
            posts=[PostWithDetailsResponse.from_orm(post) for post in posts],
            page=page,
            limit=limit,
            total=total,
        )
