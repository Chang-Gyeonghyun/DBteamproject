from fastapi import Depends
from app.entity.repository.comment import CommentRepository
from app.entity.models import Comment
from app.schemas.comment.request import CommentRequest
from app.utils.exceptions import CustomException, ExceptionEnum

class CommentService:    
    def __init__(self, comment_repository: CommentRepository = Depends()) -> None:  
        self.comment_repository = comment_repository
        
    async def create_comment(self, request: CommentRequest):
        comment = await self.comment_repository.create_comment(request)
        return comment
    
    async def delete_comment(self, user_id, comment_id):
        comment: Comment | None = await self.comment_repository.get_comment_by_id(comment_id)
        if comment.userID != user_id:
            raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
        await self.comment_repository.delete_comment(comment_id)
        return

