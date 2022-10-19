import re
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .jwt_handler import AuthHandler
from dependencies import get_db
from jwt.exceptions import PyJWTError
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
auth_handler = AuthHandler()



async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):


    try:
        payload = auth_handler.decodeJWT(token)

        if payload is None or payload == {}:
            
            raise HTTPException(status_code=401, detail="Could not validate credentials, Token is Expired",headers={"WWW-Authenticate": "Bearer"},)
        else:

            email = payload.get("email")

            user = db.query(models.User).filter_by(email=email).first()
            request.current_user = user

            return user

    except Exception as e:
        print(e, __file__)
        raise HTTPException(status_code=403, detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)
