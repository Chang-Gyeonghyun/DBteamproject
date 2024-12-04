from app.entity.repository.like import LikeRepository


class LikeService:
    def __init__(self, repository: LikeRepository):
        self.repository = repository

    async def like_post(self, user_id: str, post_id: int):
        await self.repository.like_post(user_id, post_id)

    async def unlike_post(self, user_id: str, post_id: int):
        await self.repository.unlike_post(user_id, post_id)
