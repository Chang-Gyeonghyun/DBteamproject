from fastapi import Depends
from app.entity.models import Comment
from app.entity.repository.repository import RepositoryFactory
from app.schemas.comment.request import CommentRequest
from app.utils.exceptions import CustomException, ExceptionEnum

class CommentService:    
    def __init__(self, repository_factory: RepositoryFactory = Depends()):
        self.comment_repository = repository_factory.get_comment_repository()
        
    async def create_comment(self, request: CommentRequest):
        comment = await self.comment_repository.create_comment(request)
        return comment
    
    async def delete_comment(self, user_id, comment_id):
        comment: Comment | None = await self.comment_repository.get_comment_by_id(comment_id)
        if comment.userID != user_id:
            raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
        await self.comment_repository.delete_comment(comment)
        return

