from typing import Optional
from pydantic import BaseModel, EmailStr

class RefreshToken(BaseModel):
    refresh_token: str


class CustomSchema(BaseModel):
    class Config:
        orm_mode = True


class LoginSchema(CustomSchema):
    email: EmailStr
    password: str


class RegisterRequestSchema(CustomSchema):
    name: str
    email: EmailStr
    password: str


class UserReponseSchema(CustomSchema):
    id: int
    name: str
    email: EmailStr
