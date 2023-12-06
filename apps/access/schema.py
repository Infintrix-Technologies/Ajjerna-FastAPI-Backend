from enum import Enum
from typing import Optional
from models import Role
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel, Field, validator

PydanticRole = sqlalchemy_to_pydantic(Role)



class CreateRoleSchema(BaseModel):


    name: str
    # role_for: RoleForType

    # @validator('name')
    # def name_must_contain_space(cls, v):
    #     if v is None:
    #         raise ValueError('must contain a space')
    #     return v.title()

    class Config:
        orm_mode = True




class SinglePermissionSchema(BaseModel):
    name : str
    code : str

    class Config:
        orm_mode = True

        
class CreatePermissionSchema(BaseModel):

    name : str

    class Config:
        orm_mode = True


class SetUserPermission(BaseModel):
    permission_id : int
    user_id : int

    class Config:
        orm_mode = True


class SetUserRole(BaseModel):
    role_id : int
    user_id : int

    class Config:
        orm_mode = True


class SetRolePermission(BaseModel):
    role_id : int
    permission_id : int

    class Config:
        orm_mode = True