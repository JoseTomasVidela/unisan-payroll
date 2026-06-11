from __future__ import annotations

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .config import Settings, get_settings
from .database import get_db
from .models import User
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
    def dependency(user: User = Depends(get_current_user)) -> User:
        permissions = {item.permission_code for item in user.role.permissions}
        if permission_code not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para realizar esta acción.",
            )
        return user

    return dependency

