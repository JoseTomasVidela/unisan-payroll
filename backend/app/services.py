from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Permission, Role, User
from .schemas import UserResponse
from .security import hash_password, verify_password

PERMISSIONS = {
    "payroll.read": "Consultar liquidaciones",
    "payroll.export": "Exportar liquidaciones",
    "payroll.import": "Importar archivos operacionales",
    "payroll.edit": "Editar producción diaria",
    "payroll.email": "Enviar liquidaciones por email",
    "payroll.softland": "Exportar liquidaciones a Softland",
    "rates.read": "Consultar tarifas",
    "rates.edit": "Editar tarifas",
    "workers.read": "Consultar trabajadores",
    "workers.edit": "Editar trabajadores",
    "users.manage": "Administrar usuarios",
}

ROLE_PERMISSIONS = {
    "ADMIN": tuple(PERMISSIONS),
    "RRHH": (
        "payroll.read", "payroll.export", "payroll.edit", "payroll.email",
        "payroll.softland", "rates.read", "rates.edit", "workers.read",
        "workers.edit",
    ),
    "OPERATIVO": (
        "payroll.read", "payroll.export", "payroll.import", "payroll.edit",
    ),
}


def seed_roles_and_permissions(db: Session) -> None:
    permissions: dict[str, Permission] = {}
    for code, description in PERMISSIONS.items():
        permission = db.scalar(
            select(Permission).where(Permission.permission_code == code)
        )
        if permission is None:
            permission = Permission(permission_code=code, description=description)
            db.add(permission)
        permissions[code] = permission

    db.flush()
    for role_name, permission_codes in ROLE_PERMISSIONS.items():
        role = db.scalar(select(Role).where(Role.role_name == role_name))
        if role is None:
            role = Role(role_name=role_name, description=f"Perfil {role_name}")
            db.add(role)
        role.active = True
        role.permissions = [permissions[code] for code in permission_codes]

    # Keep the legacy row only for referential integrity with historical users.
    legacy_user_role = db.scalar(select(Role).where(Role.role_name == "USER"))
    if legacy_user_role is not None:
        legacy_user_role.active = False
        legacy_user_role.permissions = []
    db.commit()


def create_user(
    db: Session,
    *,
    username: str,
    full_name: str,
    password: str,
    role_name: str,
    active: bool = True,
) -> User:
    normalized_username = username.strip().lower()
    if db.scalar(select(User).where(User.username == normalized_username)):
        raise ValueError("El nombre de usuario ya existe.")

    role = db.scalar(
        select(Role).where(Role.role_name == role_name.upper(), Role.active.is_(True))
    )
    if role is None:
        raise ValueError("El rol solicitado no existe o está inactivo.")

    user = User(
        username=normalized_username,
        full_name=full_name.strip(),
        password_hash=hash_password(password),
        role=role,
        active=active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> User | None:
    user = db.scalar(
        select(User).where(User.username == username.strip().lower())
    )
    if user is None or not user.active or not user.role.active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    user.last_login_at = datetime.utcnow()
    db.commit()
    return user


def serialize_user(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        role=user.role.role_name,
        permissions=sorted(item.permission_code for item in user.role.permissions),
        active=user.active,
    )
