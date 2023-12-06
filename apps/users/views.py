import email
from os import access
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from apps.auth.jwt_handler import AuthHandler
from apps.auth.models import User
from dependencies import get_db
from apps.auth.schema import (
    UserReponseSchema,
    RegisterRequestSchema,
    RegisterRequestSchema,
)
from sqlalchemy.exc import IntegrityError
from apps.auth.models import User

# from pymysql.err import IntegrityError
auth_handler = AuthHandler()

user_route = APIRouter()


@user_route.get("", response_model=List[UserReponseSchema])
async def list_all_users():
    return User.findAll()


@user_route.post("/new", response_model=UserReponseSchema)
async def create_new_user(
    request: RegisterRequestSchema, db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=request.email).first()

    if user and user.email == request.email:
        raise HTTPException(status_code=400, detail="Email is taken")

    hashed_password = auth_handler.get_password_hash(request.password)

    try:
        user = User()
        user.name = request.name
        user.email = request.email
        user.password = hashed_password

        user.save()

        db.refresh(user)

        return user
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Email Already Exist")


@user_route.get("/{id}", response_model=UserReponseSchema)
async def get_single_user(id):
    return User.find(id=id)


@user_route.delete("/{id}")
async def delete_user():
    User.delete()


@user_route.put("/{id}", response_model=UserReponseSchema)
async def update_user(
    id, request: RegisterRequestSchema, db: Session = Depends(get_db)
):
    try:
        user = User.find(id=id)
        user.name = request.name
        user.email = request.email
        user.password = auth_handler.get_password_hash(request.password)
        user.update()
        return user
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str("Email is already taken"))
