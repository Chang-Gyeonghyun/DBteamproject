from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_database
from app.entity.repository.attachment import AttachmentRepository
from app.entity.repository.comment import CommentRepository
from app.entity.repository.follow import FollowRepository
from app.entity.repository.keyword import KeywordRepository
from app.entity.repository.like import LikeRepository
from app.entity.repository.post import PostRepository
from app.entity.repository.user import UserRepository

class RepositoryFactory:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session
        
    def get_user_repository(self):
        return UserRepository(self.session)

    def get_post_repository(self):
        return PostRepository(self.session)

    def get_keyword_repository(self):
        return KeywordRepository(self.session)

    def get_comment_repository(self):
        return CommentRepository(self.session)
    
    def get_attachment_repository(self):
        return AttachmentRepository(self.session)
    
    def get_like_repository(self):
        return LikeRepository(self.session)
    
    def get_follow_repository(self):
        return FollowRepository(self.session)