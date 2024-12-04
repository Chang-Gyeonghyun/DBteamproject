from fastapi import APIRouter, Depends
from app.service.follow import FollowService

router = APIRouter(prefix="/follow", tags=["Follow"])


@router.post("/{user_id}")
async def follow_user(user_id: str, current_user_id: str, service: FollowService = Depends()):
    await service.follow_user(current_user_id, user_id)
    return {"message": "User followed successfully"}


@router.delete("/{user_id}")
async def unfollow_user(user_id: str, current_user_id: str, service: FollowService = Depends()):
    await service.unfollow_user(current_user_id, user_id)
    return {"message": "User unfollowed successfully"}
