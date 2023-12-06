from datetime import datetime
import email
from os import access
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from .jwt_handler import AuthHandler
from sqlalchemy.orm import Session
from apps.auth.models import User
from dependencies import get_db
from .schema import (
    RefreshToken,
    UserReponseSchema,
    RegisterRequestSchema,
    RegisterRequestSchema,
)
from sqlalchemy.exc import IntegrityError
from . import models
from .dependencies import get_current_user

auth = APIRouter()


auth_handler = AuthHandler()


@auth.post("/register", status_code=201, response_model=UserReponseSchema)
def register(request: RegisterRequestSchema, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=400, detail="Something went wrong")


@auth.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form.username).first()

    if (user is None) or (
        not auth_handler.verify_password(form.password, user.password)
    ):
        raise HTTPException(status_code=401, detail="Invalid email and/or password")
    access_token = auth_handler.access_token(user.email)
    refresh_token = auth_handler.refresh_token(user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth.post("/refresh")
def refresh_token(request: RefreshToken):
    payload = auth_handler.decodeJWT(request.refresh_token)

    if payload is None or payload == {}:
        raise HTTPException(
            status_code=401,
            detail="Please send valid payload in body",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload and payload.get("type") != "refresh":
        raise HTTPException(
            status_code=400,
            detail="Please send valid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = User.find(email=payload["email"])

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Please send valid refresh token for valid user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    is_refresh_expired = datetime.now() >= datetime.utcfromtimestamp(payload.get("exp"))

    if is_refresh_expired:
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired please login again",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_handler.access_token(user.email)
    refresh_token = auth_handler.refresh_token(user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth.get("/user-profile", response_model=UserReponseSchema)
async def user_profile(user: models.User = Depends(get_current_user)):
    return user
