from fastapi import APIRouter, Depends
from app.service.like import LikeService

router = APIRouter(prefix="/post", tags=["Likes"])


@router.post("/{post_id}/like")
async def like_post(post_id: int, user_id: str, service: LikeService = Depends()):
    await service.like_post(user_id, post_id)
    return {"message": "Post liked successfully"}


@router.delete("/{post_id}/like")
async def unlike_post(post_id: int, user_id: str, service: LikeService = Depends()):
    await service.unlike_post(user_id, post_id)
    return {"message": "Post unliked successfully"}
