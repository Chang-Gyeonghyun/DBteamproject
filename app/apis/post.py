from fastapi import APIRouter, Depends
from app.service.post import PostService
from app.schemas.post.request import PostCreateRequest, PostUpdateRequest, PostFilterRequest
from app.schemas.post.response import PostWithDetailsResponse, ListPostsResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostWithDetailsResponse)
async def create_post(post_data: PostCreateRequest, service: PostService = Depends()):
    return await service.create_post(post_data)


@router.get("/{post_id}", response_model=PostWithDetailsResponse)
async def get_post(post_id: int, service: PostService = Depends()):
    return await service.get_post(post_id)


@router.put("/{post_id}", response_model=PostWithDetailsResponse)
async def update_post(post_id: int, update_data: PostUpdateRequest, service: PostService = Depends()):
    return await service.update_post(post_id, update_data)


@router.delete("/{post_id}")
async def delete_post(post_id: int, service: PostService = Depends()):
    return await service.delete_post(post_id)


@router.get("/", response_model=ListPostsResponse)
async def filter_posts(filter_data: PostFilterRequest, service: PostService = Depends()):
    return await service.filter_posts(filter_data)


@router.get("/{user_id}/{category}", response_model=ListPostsResponse)
async def get_user_posts_by_category(
    user_id: str, category: str, page: int = 1, limit: int = 10, service: PostService = Depends()
):
    return await service.get_user_posts_by_category(user_id, category, page, limit)
