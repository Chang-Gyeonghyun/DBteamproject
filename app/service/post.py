import asyncio
import os
from typing import List
import aiofiles
from fastapi import Depends, UploadFile
from sqlalchemy.inspection import inspect
from app.entity.models import Comment, Post
from app.entity.repository.repository import RepositoryFactory
from app.schemas.post.request import MainFilterSearch, PaginatedRequest, PostCreateRequest, PostUpdateRequest, UserKeywordRequest
from app.schemas.post.response import AttachmentResponse, CommentResponse, ListPostsResponse, PostResponse, PostWithDetailsResponse
from app.utils.exceptions import CustomException, ExceptionEnum

class PostService:
    def __init__(self, repository_factory: RepositoryFactory = Depends()):
        self.post_repo = repository_factory.get_post_repository()
        self.keyword_repo = repository_factory.get_keyword_repository()
        self.attach_repo = repository_factory.get_attachment_repository()
        self.like_repo = repository_factory.get_like_repository()

    async def create_post(self, post_data: PostCreateRequest, files: List[UploadFile]):
        post: Post = await self.post_repo.create_post(post_data)
        if files:
            await asyncio.gather(
                self.save_files(files),                     
                self.attach_repo.create_attachment(post.postID, files) 
            )
        await self.keyword_repo.create_keyword(post.postID, post_data)
        return

    async def get_post(self, post_id: int, user_id: str) -> PostWithDetailsResponse:
        post = await self.post_repo.get_post_detail_by_id(post_id)
        if not post:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        
        like_state = await self.like_repo.check_like_state(user_id, post_id)
        hierarchical_comments = self.build_comment_hierarchy(post.comments)

        response = PostWithDetailsResponse(
            PostID=post.postID,
            Title=post.title,
            Content=post.content,
            Count_likes=post.count_likes,
            like_state=like_state,
            userID=post.user.userID,
            nickname=post.user.nickname,
            Create_at=post.create_at,
            Update_at=post.update_at,
            keyword=[kw.name for kw in post.keywords],
            attachment=[AttachmentResponse.from_orm(att) for att in post.attachments],
            comments=[
                CommentResponse(
                    commentID=comment.commentID,
                    parentcommentID=comment.parentcommentID,
                    content=comment.content,
                    userID=comment.userID,
                    nickname=comment.user.nickname, 
                    create_at=comment.create_at,
                    replies=[
                        CommentResponse(
                            commentID=reply.commentID,
                            parentcommentID=reply.parentcommentID,
                            content=reply.content,
                            userID=reply.userID,
                            nickname=reply.user.nickname,  
                            create_at=reply.create_at,
                            replies=[],
                        )
                        for reply in comment.replies
                    ],
                )
                for comment in hierarchical_comments
            ],
        )
        return response
    
    def build_comment_hierarchy(self, comments: List[Comment]):
        comment_map = {comment.commentID: comment for comment in comments}
        root_comments = []

        for comment in comments:
            if comment.parentcommentID:
                parent = comment_map.get(comment.parentcommentID)
                if parent:
                    if not hasattr(parent, "replies"):
                        parent.replies = []
                    parent.replies.append(comment)
            else:
                root_comments.append(comment)

        return root_comments

    async def update_post(self, post_id: int, update_data: PostUpdateRequest, files: List[UploadFile]):
        post: Post = await self.post_repo.get_post_by_id(post_id)
        if not post:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        filtered_data = self.filter_valid_fields(Post, update_data)
        await self.post_repo.update_post(post_id, filtered_data)

        if files:
            file_paths = await self.attach_repo.delete_attachments_by_post_id(post_id)
            await self.delete_files(file_paths)
            await asyncio.gather(
                self.save_files(files),
                self.attach_repo.create_attachment(post_id, files)
            )
        if update_data.keywords:
            await self.keyword_repo.delete_keywords_by_post_id(post_id)
            await self.keyword_repo.create_keyword(post_id, update_data)
        return

    def filter_valid_fields(self, model, data: PostUpdateRequest) -> dict:
        mapper = inspect(model)
        valid_fields = {column.key for column in mapper.attrs}
        data_dict = data.dict(exclude_unset=True)  # unset된 값 제외
        filtered_data = {}
        for key, value in data_dict.items():
            if key in valid_fields:
                if isinstance(value, (list, dict)):
                    continue
                else:
                    filtered_data[key] = value
        return filtered_data


    async def delete_post(self, post_id: int, user_id: str) -> None:
        post: Post = await self.post_repo.get_post_by_id(post_id)
        if not post:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        if post.userID != user_id:
            raise CustomException(ExceptionEnum.USER_UNAUTHORIZED)
        
        await self.post_repo.delete_post(post)
        return

    async def trending_posts(self, filter_data: PaginatedRequest) -> ListPostsResponse:
        posts, total = await self.post_repo.treding_posts(filter_data)
        response_posts = [
            PostResponse(
                postID=post.postID,
                title=post.title,
                count_likes=post.count_likes,
                userID=post.user.userID,
                nickname=post.user.nickname,
                create_at=post.create_at,
            )
            for post in posts
        ]

        return ListPostsResponse(
            posts=response_posts,
            page=filter_data.page,
            limit=filter_data.limit,
            total=total,
        )

    async def get_user_posts_by_category(self, request: UserKeywordRequest) -> ListPostsResponse:
        posts, total = await self.post_repo.get_user_posts_by_category(request)
        response_posts = [
            PostResponse(
                postID=post.postID,
                title=post.title,
                count_likes=post.count_likes,
                userID=post.user.userID,
                nickname=post.user.nickname,
                create_at=post.create_at,
            )
            for post in posts
        ]

        return ListPostsResponse(
            posts=response_posts,
            page=request.page,
            limit=request.limit,
            total=total,
        )

    async def get_posts_by_filtering(self, request: MainFilterSearch) -> ListPostsResponse:
        posts, total = await self.post_repo.get_posts_by_filtering(request)
        response_posts = [
            PostResponse(
                postID=post.postID,
                title=post.title,
                count_likes=post.count_likes,
                userID=post.user.userID,
                nickname=post.user.nickname,
                create_at=post.create_at,
            )
            for post in posts
        ]

        return ListPostsResponse(
            posts=response_posts,
            page=request.page,
            limit=request.limit,
            total=total,
        )

    async def save_files(self, files: List[UploadFile]) -> List[str]:
        upload_dir = "./uploads/attachments"
        for file in files:
                file_path = os.path.join(upload_dir, file.filename)
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(await file.read())  
        return
    
    async def delete_files(file_paths: List[str]):
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)