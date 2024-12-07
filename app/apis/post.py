from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile
from app.service.post import PostService
from app.schemas.post.request import PaginatedRequest, PostCreateRequest, PostUpdateRequest, UserKeywordRequest
from app.schemas.post.response import PostWithDetailsResponse, ListPostsResponse
from app.apis.user import oauth2_scheme
from app.service.user import UserService
from app.utils.exceptions import CustomException, ExceptionEnum

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", status_code=201)
async def create_post(
    post_data: PostCreateRequest = Depends(PostCreateRequest.as_form),
    files: Optional[List[UploadFile]] = File(None),
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    post_service: PostService = Depends(),
):
    user_id: str = user_service.decode_jwt(token)
    if user_id != post_data.user_id:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    return await post_service.create_post(post_data, files)

@router.get("/trending", response_model=ListPostsResponse)
async def trending_posts(
    filter_data: PaginatedRequest = Depends(), 
    post_service: PostService = Depends()
):
    return await post_service.trending_posts(filter_data)


@router.get("/{post_id}", response_model=PostWithDetailsResponse)
async def get_post(post_id: int, post_service: PostService = Depends()):
    return await post_service.get_post(post_id)


@router.put("/{post_id}")
async def update_post(
    post_id: int,                       
    update_data: PostUpdateRequest = Depends(PostUpdateRequest.as_form),                       
    files: Optional[List[UploadFile]] = File(None),
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    post_service: PostService = Depends()
):
    user_id: str = user_service.decode_jwt(token) 
    if user_id != update_data.user_id:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    return await post_service.update_post(post_id, update_data, files)


@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,                                          
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    post_service: PostService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    return await post_service.delete_post(post_id, user_id)

@router.get("/{user_id}/{keyword}", response_model=ListPostsResponse)
async def get_user_posts_by_category(
    request: UserKeywordRequest = Depends(),
    post_service: PostService = Depends()
):
    return await post_service.get_user_posts_by_category(request)
