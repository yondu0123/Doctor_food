from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models.user import UserRole


# 회원가입 요청
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole
    phone: Optional[str] = None


# 로그인 요청
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 토큰 응답
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 사용자 응답
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: UserRole
    oauth_provider: Optional[str]
    profile_image: Optional[str]
    
    class Config:
        from_attributes = True


# OAuth 로그인 요청
class OAuthLogin(BaseModel):
    code: str
    redirect_uri: str
