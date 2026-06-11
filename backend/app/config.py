from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    database_url: str
    db_ssl_ca: str | None
    jwt_secret: str
    access_token_minutes: int
    bootstrap_admin_username: str | None
    bootstrap_admin_password: str | None
    bootstrap_admin_name: str
    cors_origins: tuple[str, ...]


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "PAYROLL_DATABASE_URL",
            "sqlite:///./payroll_dev.db",
        ),
        db_ssl_ca=os.getenv("PAYROLL_DB_SSL_CA") or None,
        jwt_secret=os.getenv("PAYROLL_JWT_SECRET", "development-secret-change-me"),
        access_token_minutes=int(os.getenv("PAYROLL_ACCESS_TOKEN_MINUTES", "480")),
        bootstrap_admin_username=os.getenv("PAYROLL_BOOTSTRAP_ADMIN_USERNAME"),
        bootstrap_admin_password=os.getenv("PAYROLL_BOOTSTRAP_ADMIN_PASSWORD"),
        bootstrap_admin_name=os.getenv(
            "PAYROLL_BOOTSTRAP_ADMIN_NAME",
            "Administrador",
        ),
        cors_origins=_split_csv(
            os.getenv(
                "PAYROLL_CORS_ORIGINS",
                "http://localhost:5500,http://127.0.0.1:5500",
            )
        ),
    )

