from typing import List
from apps.auth.dependencies import get_current_user
from fastapi import Depends, HTTPException
from apps.auth import models


# def permission_required(required_perms: List, current_user: models.User = Depends(get_current_user)):


#     if not set(required_perms).issubset(current_user.all_permissions):
#         raise HTTPException(
#             status_code=403, detail="You must be Super admin to perform this action.")


# class PermissionChecker:
#     def __init__(self, permissions_required: List[str]):
#         self.permissions_required = set(permissions_required)

#     def __call__(self, q: str = ""):
#         if q:
#             return self.fixed_content in q
#         return False

#     if not set(required_perms).issubset(current_user.all_permissions):
#         raise HTTPException(
#             status_code=403, detail="You must be Super admin to perform this action.")
