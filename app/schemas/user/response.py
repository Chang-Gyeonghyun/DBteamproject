import base64
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, ConfigDict
   
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    
class UserInformation(BaseModel):
    userID: str
    email: str
    phone: str
    gender: str
    birth: str
    name: str
    nickname: str
    introduce: Optional[str] | None
    profile_image: Optional[str] | None
    
    class Config:
        orm_mode = True
    @property
    def profile_image_base64(self) -> Optional[str]:
        if self.profile_image:
            try:
                with open(self.profile_image, "rb") as image_file:
                    return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
            except FileNotFoundError:
                return None
        return None

class FollowResponse(BaseModel):
    userID: str
    nickname: str
    profileImage: Optional[str] = None  
    follow_at: datetime  

    
class ListFollowResponse(BaseModel):
    follow: List[FollowResponse]
    page: int
    limit: int
    total: int

class UserBlogResponse(BaseModel):
    userID: str
    nickname: str
    follow_state: bool
    keyword_count: Dict[str, int]
    total_posts: int