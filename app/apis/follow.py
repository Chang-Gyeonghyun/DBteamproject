from fastapi import APIRouter, Depends
from app.service.follow import FollowService
from app.apis.user import oauth2_scheme
from app.service.user import UserService

router = APIRouter(prefix="/follow", tags=["Follow"])

@router.post("/{userID}")
async def follow_user(
    userID: str,                                          
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    follow_service: FollowService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    await follow_service.follow_user(user_id, userID)
    return

@router.delete("/{user_id}")
async def unfollow_user(
    userID: str,                                          
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    follow_service: FollowService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    await follow_service.unfollow_user(user_id, userID)
    return
