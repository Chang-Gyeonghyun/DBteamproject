from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.entity.user.document import User
from app.schemas.user.request import UserSignUp, UserUpdate
from app.schemas.user.response import LoginResponse, UserInformation
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
    request: UserSignUp,
    user_service: UserService = Depends()
):
    return await user_service.create_user_service(request)

@router.get("/{UserID}", response_model=UserInformation)
async def get_user_info(
    UserID: str,
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    if user_id != UserID:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    user: User = user_service.get_user_info(user_id)
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

@router.get("/{UserID}/likes", response_model=None)
async def get_user_likes():
    pass

@router.get("/{UserID}/follower", response_model=None)
async def get_user_follower():
    pass

@router.get("/{UserID}/following", response_model=None)
async def get_user_following():
    pass