from __future__ import annotations

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import Settings, get_settings
from .database import get_db
from .models import PayrollSetting, User
from .security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o vencidas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        user_id = decode_access_token(credentials.credentials, settings)
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise unauthorized

    user = db.get(User, user_id)
    if user is None or not user.active or not user.role.active:
        raise unauthorized
    return user


def require_permission(permission_code: str):
    def dependency(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        permissions = {item.permission_code for item in user.role.permissions}
        if permission_code not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para realizar esta acción.",
            )
        if permission_code == "payroll.edit":
            setting = db.scalar(
                select(PayrollSetting).where(
                    PayrollSetting.setting_key == "operations_edit_locked"
                )
            )
            if setting is not None and setting.setting_value.casefold() == "true":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Las planillas están bloqueadas. Abra el candado para realizar cambios.",
                )
        return user

    return dependency

