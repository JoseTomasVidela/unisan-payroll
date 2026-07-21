from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from .config import Settings

PBKDF2_ITERATIONS = 600_000


def validate_password(password: str) -> str:
    if len(password) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres.")
    if not any(character.isupper() for character in password):
        raise ValueError("La contraseña debe incluir una mayúscula.")
    if not any(character.islower() for character in password):
        raise ValueError("La contraseña debe incluir una minúscula.")
    if not any(not character.isalnum() for character in password):
        raise ValueError("La contraseña debe incluir un carácter especial.")
    return password


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return "pbkdf2_sha256${}${}${}".format(
        PBKDF2_ITERATIONS,
        base64.urlsafe_b64encode(salt).decode("ascii"),
        base64.urlsafe_b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt_text, digest_text = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.urlsafe_b64decode(salt_text.encode("ascii"))
        expected = base64.urlsafe_b64decode(digest_text.encode("ascii"))
        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int, settings: Settings) -> tuple[str, int]:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=settings.access_token_minutes)
    token = jwt.encode(
        {"sub": str(user_id), "iat": now, "exp": expires, "type": "access"},
        settings.jwt_secret,
        algorithm="HS256",
    )
    return token, settings.access_token_minutes * 60


def decode_access_token(token: str, settings: Settings) -> int:
    payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Tipo de token inválido.")
    return int(payload["sub"])

