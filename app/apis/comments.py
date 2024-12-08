from fastapi import APIRouter, Depends
from app.schemas.comment.request import CommentRequest
from app.service.comment import CommentService
from app.service.user import UserService
from app.utils.exceptions import CustomException, ExceptionEnum
from app.apis.user import oauth2_scheme

router = APIRouter(prefix="/comments", tags=['Comments'])

@router.post("/", status_code=201)
async def user_login(
    request: CommentRequest,
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    comment_service: CommentService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    if request.userID != user_id:
        raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
    await comment_service.create_comment(request)
    return
    

@router.delete("/{CommentID}", status_code=204)
async def user_login(
    CommentID=int,
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
    comment_service: CommentService = Depends()
):
    user_id: str = user_service.decode_jwt(token)
    await comment_service.delete_comment(user_id, CommentID)
    return