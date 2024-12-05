from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.entity.models import User
from app.schemas.post.response import ListPostsResponse
from app.schemas.user.request import PaginationParams, UserSignUp, UserUpdate
from app.schemas.user.response import ListFollowResponse, LoginResponse, UserInformation
from app.service.user import UserService
from app.utils.exceptions import CustomException, ExceptionEnum

router = APIRouter(prefix="/user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.post("/login", response_model=LoginResponse)
async def user_login(
    request: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends()
):
    return await user_service.user_login_service(request)
    
@router.post("/signup", status_code=201)
async def user_signup(
    request: UserSignUp = Depends(),
    profileImage: Optional[UploadFile] = File(None),
    user_service: UserService = Depends()
):
    return await user_service.create_user_service(request, profileImage)

@router.get("/{UserID}", response_model=UserInformation)
async def get_user_info(
    UserID: str,
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    if user_id != UserID:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    user: User = await user_service.get_user_info(user_id)
    return user

@router.put("/{UserID}")
async def modify_user_info(
    UserID: str,
    request: UserUpdate,
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    if user_id != UserID:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    await user_service.update_user_info(user_id, request)
    return

@router.delete("/{UserID}", status_code=204)
async def delete_user_info(
    UserID: str,
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    if user_id != UserID:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    await user_service.delete_user_service(user_id)
    return

@router.get("/{UserID}/likes", response_model=ListPostsResponse)
async def get_user_likes(
    UserID: str,
    page_param: PaginationParams = Depends(),
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    if user_id != UserID:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    return await user_service.get_userlike_post(user_id, page_param)
    
    

@router.get("/{UserID}/follower", response_model=ListFollowResponse)
async def get_user_follower(
    UserID: str,
    page_param: PaginationParams = Depends(),
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    if user_id != UserID:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    return await user_service.get_user_follower(user_id, page_param)
    

@router.get("/{UserID}/following", response_model=ListFollowResponse)
async def get_user_following(
    UserID: str,
    page_param: PaginationParams = Depends(),
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    if user_id != UserID:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    return await user_service.get_user_following(user_id, page_param)