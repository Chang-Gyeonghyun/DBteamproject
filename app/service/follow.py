from fastapi import Depends
from app.entity.repository.follow import FollowRepository
from app.entity.repository.repository import RepositoryFactory
from app.utils.exceptions import CustomException, ExceptionEnum


class FollowService:
    def __init__(self, repository_factory: RepositoryFactory = Depends()):
        self.user_repository = repository_factory.get_user_repository()
        self.follow_repository = repository_factory.get_follow_repository()

    async def follow_user(self, user_id: str, follow_id: str):
        user = await self.user_repository.search_user_by_id(follow_id)
        if not user:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        await self.follow_repository.follow_user(user_id, follow_id)
        return

    async def unfollow_user(self, user_id: str, follow_id: str):
        user = await self.user_repository.search_user_by_id(follow_id)
        if not user:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        await self.follow_repository.get_follow(user_id, follow_id)
        await self.follow_repository.unfollow_user(user_id, follow_id)
        return