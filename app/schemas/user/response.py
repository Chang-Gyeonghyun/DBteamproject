from pydantic import BaseModel
   
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    
class UserInformation(BaseModel):
    userID: int
    email: str
    phone: str
    gender: str
    birth: str
    name: str
    nickname: str
    introduce: str
    profileImage: str
    