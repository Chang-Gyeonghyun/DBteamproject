from fastapi import APIRouter, Depends
from app.service.like import LikeService
from app.apis.user import oauth2_scheme
from app.service.user import UserService

router = APIRouter(prefix="/post", tags=["Likes"])


@router.post("/{post_id}/like")
async def like_post(
    post_id: int,                                          
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    like_service: LikeService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    await like_service.like_post(user_id, post_id)
    return


@router.delete("/{post_id}/like")
async def unlike_post(
    post_id: int,                                          
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    like_service: LikeService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    await like_service.unlike_post(user_id, post_id)
    return