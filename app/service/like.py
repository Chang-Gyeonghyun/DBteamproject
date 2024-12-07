from fastapi import Depends
from app.entity.models import Post
from app.entity.repository.repository import RepositoryFactory
from app.utils.exceptions import CustomException, ExceptionEnum


class LikeService:
    def __init__(self, repository_factory: RepositoryFactory = Depends()):
        self.like_repository = repository_factory.get_like_repository()
        self.post_repository = repository_factory.get_post_repository()

    async def like_post(self, user_id: str, post_id: int):
        post: Post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        await self.post_repository.update_likes(post_id)
        await self.like_repository.like_post(user_id, post_id)

    async def unlike_post(self, user_id: str, post_id: int):
        post: Post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        await self.post_repository.update_likes(post_id, unlike=True)
        await self.like_repository.unlike_post(user_id, post_id)
