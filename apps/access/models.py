import sqlalchemy as sa
from sqlalchemy.orm import relationship
from database import Base, BaseModel




# roles_permissions_association_table = sa.Table('roles_permissions', Base.metadata,
#                                                sa.Column(
#                                                    'role_id', sa.ForeignKey('roles.id')),
#                                                sa.Column('permission_id', sa.ForeignKey(
#                                                    'permissions.id'))
#                                                )
class Role(BaseModel):
    __tablename__ = "roles"
    name = sa.Column(sa.String(50), nullable=False, unique=True)
    permissions = relationship("Permission", secondary='roles_permissions', backref=sa.orm.backref('role_permission', lazy='dynamic'))



    def __repr__(self) -> str:
        return f"Role: {self.name}"


class Permission(BaseModel):
    __tablename__ = "permissions"
    name = sa.Column(sa.String(50), nullable=False, unique=True)
    code = sa.Column(sa.String(50), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"(Permission: {self.code})"


class RolesPermissionsAssociation(BaseModel):
    __tablename__ = "roles_permissions"
    role_id= sa.Column(sa.ForeignKey('roles.id'))
    permission_id = sa.Column(sa.ForeignKey('permissions.id'))
    

    __table_args__ = (sa.UniqueConstraint('role_id', 'permission_id', name='_role_permission_uc'),
                     )

class UserRolesAssociation(BaseModel):
    __tablename__ = "user_roles"

    user_id= sa.Column(sa.ForeignKey('users.id'))
    role_id = sa.Column(sa.ForeignKey('roles.id'))

    __table_args__ = (sa.UniqueConstraint('role_id', 'user_id', name='_role_user_uc'),
                     )


class UserPermissionsAssociation(BaseModel):
    __tablename__ = "user_permissions"
    user_id= sa.Column(sa.ForeignKey('users.id'))
    permission_id = sa.Column(sa.ForeignKey('permissions.id'))

    __table_args__ = (sa.UniqueConstraint('user_id', 'permission_id', name='_user_permission_uc'),
                     )