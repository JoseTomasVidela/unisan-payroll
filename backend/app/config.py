from __future__ import annotations

import os
import json
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _local_smtp_settings() -> dict[str, str]:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        values: dict[str, str] = {}
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
        mapped = {
            "host": values.get("PAYROLL_SMTP_HOST"),
            "port": values.get("PAYROLL_SMTP_PORT"),
            "username": values.get("PAYROLL_SMTP_USERNAME"),
            "password": values.get("PAYROLL_SMTP_PASSWORD"),
            "sender": values.get("PAYROLL_SMTP_FROM"),
            "recipient": values.get("PAYROLL_SMTP_TEST_RECIPIENT"),
        }
        if all(mapped.values()):
            return {key: str(value) for key, value in mapped.items() if value}
    config_path = Path(__file__).resolve().parents[1] / ".smtp.local.ps1"
    if os.name != "nt" or not config_path.exists():
        return {}
    escaped_path = str(config_path).replace("'", "''")
    command = (
        f". '{escaped_path}'; "
        "[pscustomobject]@{"
        "host=$env:PAYROLL_SMTP_HOST;port=$env:PAYROLL_SMTP_PORT;"
        "username=$env:PAYROLL_SMTP_USERNAME;password=$env:PAYROLL_SMTP_PASSWORD;"
        "sender=$env:PAYROLL_SMTP_FROM;recipient=$env:PAYROLL_SMTP_TEST_RECIPIENT"
        "}|ConvertTo-Json -Compress"
    )
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", command],
            capture_output=True,
            check=True,
            text=True,
            timeout=15,
        )
        return {key: str(value) for key, value in json.loads(result.stdout).items() if value}
    except (OSError, subprocess.SubprocessError, ValueError, json.JSONDecodeError):
        return {}


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
    smtp_host: str = "mail.unisan.cl"
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    smtp_test_recipient: str | None = None


@lru_cache
def get_settings() -> Settings:
    local_smtp = _local_smtp_settings()
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
        smtp_host=local_smtp.get("host") or os.getenv("PAYROLL_SMTP_HOST", "mail.unisan.cl"),
        smtp_port=int(local_smtp.get("port") or os.getenv("PAYROLL_SMTP_PORT", "587")),
        smtp_username=local_smtp.get("username") or os.getenv("PAYROLL_SMTP_USERNAME"),
        smtp_password=local_smtp.get("password") or os.getenv("PAYROLL_SMTP_PASSWORD"),
        smtp_from=local_smtp.get("sender") or os.getenv("PAYROLL_SMTP_FROM"),
        smtp_test_recipient=local_smtp.get("recipient") or os.getenv("PAYROLL_SMTP_TEST_RECIPIENT"),
    )

