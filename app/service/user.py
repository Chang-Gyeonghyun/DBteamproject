import math
import os
from typing import Dict, List, Tuple
from uuid import uuid4
import bcrypt
from fastapi import Depends, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta

from sqlalchemy import func, select

from app.entity.models import Keyword, Post, User
from app.entity.repository.repository import RepositoryFactory
from app.schemas.post.response import ListPostsResponse, PostResponse
from app.schemas.user.request import PaginationParams, UserSignUp, UserUpdate
from app.schemas.user.response import FollowResponse, UserBlogResponse, ListFollowResponse, LoginResponse
from app.utils.exceptions import CustomException, ExceptionEnum

class UserService:
    encoding = "UTF-8"
    jwt_algorithm = "HS256"
    secret_key = "b8394efc3c1d4838a71587c4b6aef2fb1a62dcbf4d9e4c4b8bfa86c279d768d4"
        
    def __init__(self, repository_factory: RepositoryFactory = Depends()) -> None:  
        self.user_repository = repository_factory.get_user_repository()
        self.follow_repository = repository_factory.get_follow_repository()
        
    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), 
            bcrypt.gensalt()
        )
        return hashed_password.decode("UTF-8")
    
    def verfiy_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(self.encoding),
                              hashed_password.encode(self.encoding))
        
    async def create_user_service(self, user_form: UserSignUp, profileImage):
        user: User | None = await self.user_repository.search_user_by_id(user_form.userID)
        if user:
            raise CustomException(ExceptionEnum.USER_EXISTS)
        hashed_pw = self.hash_password(user_form.password)
        user_form.password = hashed_pw
        
        profile_image = await self.save_user_profile_image(profileImage)
        user_form.profile_image = profile_image
        await self.user_repository.create_user_entity(user_form)
        return
    
    async def user_login_service(self, login_form: OAuth2PasswordRequestForm):
        user: User | None = await self.user_repository.search_user_by_id(login_form.username)
        if user and self.verfiy_password(login_form.password, user.hashed_password):
            access_token = self.create_jwt(login_form.username)
            return LoginResponse(access_token=access_token, token_type="bearer")
        raise CustomException(ExceptionEnum.LOGIN_FAILED)
    
    async def update_user_info(self, user_id, user_form: UserUpdate, profileImage: UploadFile):
        user: User | None = await self.user_repository.search_user_by_id(user_id)
        if not user:
            raise CustomException(ExceptionEnum.USER_NOT_FOUND)
        profile_image = await self.save_user_profile_image(profileImage)
        user_form.profile_image = profile_image
        await self.user_repository.update_user(user, user_form)
        return

    async def delete_user_service(self, user_id):
        user: User | None = await self.user_repository.search_user_by_id(user_id)
        if user:
            await self.user_repository.delete_user(user)
            return
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)

    async def get_user_info(self, user_id):
        user: User = await self.user_repository.search_user_by_id(user_id)
        if user: 
            return user
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    
    async def get_user_follower(self, user_id: str, page_param: PaginationParams):
        paged_follow: List[Tuple[User, str]] | None = await self.user_repository.get_user_follower(user_id, page_param)
        total_follow: List[Tuple[User, str]] | None = await self.user_repository.get_user_follower(user_id)
        total_pages = math.ceil(len(total_follow) / page_param.limit)
        page_size = page_param if paged_follow else len(paged_follow)
        follower_list = [
            FollowResponse(
                userID=user.userID,
                nickname=user.nickname,
                profile_image=user.profile_image,
                follow_at=follow_at,
            )
            for user, follow_at in paged_follow
        ]
        return ListFollowResponse(
            follow=follower_list, 
            page=page_param.page, 
            limit=page_size,
            total=total_pages
        )

    async def save_user_profile_image(self, profileImage: UploadFile) -> str:
        if profileImage:            
            save_dir = "uploads/profile_images"
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, profileImage.filename)

            with open(save_path, "wb") as f:
                file_content = await profileImage.read()
                f.write(file_content)

            return save_path
        return ""
    
    async def get_user_following(self, user_id: str, page_param: PaginationParams):
        paged_follow: List[Tuple[User, str]] | None = await self.user_repository.get_user_following(user_id, page_param)
        total_follow: List[Tuple[User, str]] | None = await self.user_repository.get_user_following(user_id)
        
        total_pages = math.ceil(len(total_follow) / page_param.limit) if total_follow else 0
        page_size = len(paged_follow) if paged_follow else 0
        
        following_list = [
            FollowResponse(
                userID=user.userID,
                nickname=user.nickname,
                profile_image=user.profile_image,
                follow_at=follow_at,
            )
            for user, follow_at in paged_follow
        ]
        
        return ListFollowResponse(
            follow=following_list, 
            page=page_param.page, 
            limit=page_size,
            total=total_pages
        )


    async def get_userlike_post(self, user_id: str, page_param: PaginationParams):
        paged_posts: List[Post] | None = await self.user_repository.get_user_likes(user_id, page_param)
        total_posts: List[Post] | None = await self.user_repository.get_user_likes(user_id)
        total_pages = math.ceil(len(total_posts) / page_param.limit)
        page_size = page_param if paged_posts else len(paged_posts)
        liked_posts = [
            PostResponse(
                PostID=post.postID,
                Title=post.title,
                Count_likes=post.count_likes,
                Create_at=post.create_at
            )
            for post in paged_posts
        ]
        return ListPostsResponse(
            posts=liked_posts, 
            page=page_param.page, 
            limit=page_size, 
            total=total_pages
        )

    async def get_user_blog_main(self, user_id: str, current_id: str) -> UserBlogResponse:
        user = await self.user_repository.search_user_by_id(user_id)
        keyword_count = await self.user_repository.get_keyword_post_count(user_id)
        total_count = await self.user_repository.get_total_post_count(user_id)
        follow = await self.follow_repository.get_follow(current_id, user_id)
        follow_state = follow is not None
        return UserBlogResponse(
            userID=user.userID,
            nickname=user.nickname,
            follow_state=follow_state,
            keyword_count=keyword_count, 
            total_posts=total_count
        )


    def create_jwt(self, userID: str) -> str:
        return jwt.encode(
            {
                "sub": userID,
                "exp": datetime.now() + timedelta(days=1)
            }, 
            self.secret_key, algorithm=self.jwt_algorithm
        )
    
    def decode_jwt(self, access_token: str):
        try:
            payload: dict = jwt.decode(
                access_token, 
                self.secret_key, 
                algorithms=[self.jwt_algorithm]
            )
            user_id = payload.get('sub')
            if not user_id:
                raise CustomException(ExceptionEnum.INVALID_TOKEN)
            return user_id
        except ExpiredSignatureError:
            raise CustomException(ExceptionEnum.TOKEN_EXPIRED)
        except JWTError:
            raise CustomException(ExceptionEnum.INVALID_TOKEN)