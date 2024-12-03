from typing import List, Optional
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
    
class FollowResponse(BaseModel):
    userID: str
    nickname: str
    profileImage: str
    follow_at: str
    
class ListFollowResponse(BaseModel):
    follow: List[FollowResponse]
    page: int
    limit: int
    total: int