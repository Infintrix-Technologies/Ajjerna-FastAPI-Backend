from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from database import BaseModel
from dependencies import get_db, return_db
from sqlalchemy.orm import Session

class User(BaseModel):
    __tablename__ = "users"

    name = sa.Column(sa.String(75))
    email = sa.Column(sa.String(100), unique=True, nullable=True)
    password = sa.Column(sa.String(255))



    @classmethod
    async def get_user(cls, email):
        db = return_db()
        query = db.query(cls).filter_by(email=email).first()
        return query

    def verify_password(self, password):
        return True
