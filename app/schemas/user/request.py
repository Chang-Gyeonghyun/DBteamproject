from typing import Optional
from pydantic import BaseModel, create_model
from fastapi import Query, Form, File, UploadFile

class UserUpdate(BaseModel):
    userID: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birth: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    introduce: Optional[str] = None
    profile_image: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        userID: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        gender: Optional[str] = Form(None),
        birth: Optional[str] = Form(None),
        name: Optional[str] = Form(None),
        nickname: Optional[str] = Form(None),
        introduce: Optional[str] = Form(None),
        profile_image: Optional[str] = Form(None),
    ):
        return cls(
            userID=userID,
            email=email,
            phone=phone,
            gender=gender,
            birth=birth,
            name=name,
            nickname=nickname,
            introduce=introduce,
            profile_image=profile_image,
        )

class UserSignUp(BaseModel):
    userID: str
    email: str
    password: str
    phone: str
    gender: str
    birth: str
    name: str
    nickname: str
    introduce: Optional[str] = None
    profile_image: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        userID: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        phone: str = Form(...),
        gender: str = Form(...),
        birth: str = Form(...),
        name: str = Form(...),
        nickname: str = Form(...),
        introduce: Optional[str] = Form(None),
        profile_image: Optional[str] = Form(None)
    ):
        return cls(
            userID=userID,
            email=email,
            password=password,
            phone=phone,
            gender=gender,
            birth=birth,
            name=name,
            nickname=nickname,
            introduce=introduce,
            profile_image=profile_image
        )


class PaginationParams(BaseModel):
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)")
    limit: int = Query(10, ge=1, le=100, description="한 페이지당 항목 수 (1-100)")