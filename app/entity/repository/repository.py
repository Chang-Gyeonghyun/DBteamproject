from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.repository.attachment import AttachmentRepository
from app.entity.repository.keyword import KeywordRepository
from app.entity.repository.post import PostRepository

class RepositoryFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_post_repository(self):
        return PostRepository(self.session)

    def get_keyword_repository(self):
        return KeywordRepository(self.session)

    def get_attachment_repository(self):
        return AttachmentRepository(self.session)