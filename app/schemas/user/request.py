from typing import Optional
from pydantic import BaseModel

class UserUpdate(BaseModel):
    userID: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birth: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    introduce: Optional[str] = None
    profileImage: Optional[str] = None

class UserSignUp(BaseModel):
    userID: str
    email: str
    password: str
    phone: str
    gender: str
    birth: str
    name: str
    nickname: str
    introduce: str
    profileImage: str