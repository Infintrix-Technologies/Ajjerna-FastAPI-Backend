from typing import List
from urllib import request
from fastapi import APIRouter, Depends, HTTPException, Request
from dependencies import get_db

from . import models as access_models, schema
from apps.auth import models as auth_models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from apps.auth.dependencies import get_current_user
# from .dependencies import permission_required
access = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@access.post("/role/add",
             # dependencies=[Depends(permission_required(["add_role"]))]
             )
async def create_role(request: schema.CreateRoleSchema):
    role = access_models.Role()
    role.name = request.name
    role.save()


@access.get("/roles")
async def list_roles():
    roles = access_models.Role.findAll()
    return roles


@access.delete("/role/{id}")
async def delete_role(id):
    role = access_models.Role.find(id=id)
    role.delete()


@access.get("/role/{id}")
async def get_role(id):
    role = access_models.Role.find(id=id)
    return role


@access.put("/role/{id}")
async def update_role(id, request: schema.CreateRoleSchema):
    role = access_models.Role.find(id=id)

    role.update_dynamic(**request.dict())

    return role


@access.post("/permission/add")
async def create_permission(request: schema.CreatePermissionSchema, db: Session = Depends(get_db)):
    permission = access_models.Permission()
    permission.name = request.name
    permission.code = str(request.name).lower().replace(
        "can ", "").replace(" ", "_")
    permission.save()


@access.get("/permissions")
async def list_permissions():
    permissions = access_models.Permission.findAll()
    return permissions


@access.delete("/permission/{id}")
async def delete_permission(id):
    permission = access_models.Permission.find(id=id)
    permission.delete()


@access.get("/permission/{id}")
async def get_permission(id):
    permission = access_models.Permission.find(id=id)
    return permission


@access.put("/permission/{id}")
async def update_permission(id, request: schema.CreatePermissionSchema):
    permission = access_models.Permission.find(id=id)

    permission.update_dynamic(**request.dict())

    return permission


@access.get("/my-permissions")
def my_permissions(request: Request):
    return request.current_user.all_permissions


@access.get("/my-roles")
def my_roles(request: Request):
    return [role.permissions for role in request.current_user.roles]


@access.post("/set_role_permission")
async def set_role_permission(set_role_permission_schema: schema.SetRolePermission):
    role = access_models.Role.find(id=set_role_permission_schema.role_id)
    permission = access_models.Permission.find(
        id=set_role_permission_schema.permission_id)
    permission_role = access_models.RolesPermissionsAssociation()
    permission_role.permission_id = permission.id
    permission_role.role_id = role.id

    permission_role.save(
        f"Permission {permission.code} is assigned to {role.name}")


@access.post("/set_user_permission")
async def set_user_permission(set_user_permission_schema: schema.SetUserPermission):
    permission = access_models.Permission.find(
        id=set_user_permission_schema.permission_id)
    user = auth_models.User.find(id=set_user_permission_schema.user_id)

    user_permission = access_models.UserPermissionsAssociation()
    user_permission.user_id = user.id
    user_permission.permission_id = permission.id

    user_permission.save(
        f"Permission {permission.code} is assigned to {user.username}")


@access.post("/set_user_role")
async def set_user_role(set_user_role_schema: schema.SetUserRole):
    role = access_models.Role.find(id=set_user_role_schema.role_id)
    user = auth_models.User.find(id=set_user_role_schema.user_id)

    user_role = access_models.UserRolesAssociation()
    user_role.user_id = user.id
    user_role.role_id = role.id

    user_role.save(f"Role {role.name} is assigned to {user.username}")
