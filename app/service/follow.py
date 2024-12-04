from app.entity.repository.follow import FollowRepository


class FollowService:
    def __init__(self, repository: FollowRepository):
        self.repository = repository

    async def follow_user(self, user_id: str, follow_id: str):
        await self.repository.follow_user(user_id, follow_id)

    async def unfollow_user(self, user_id: str, follow_id: str):
        await self.repository.unfollow_user(user_id, follow_id)
