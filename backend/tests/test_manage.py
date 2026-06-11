from argparse import Namespace
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.models import User
from app.security import verify_password


def test_create_admin_command(monkeypatch, tmp_path: Path):
    database_path = tmp_path / "manage.db"
    database_url = f"sqlite:///{database_path.as_posix()}"
    monkeypatch.setenv("PAYROLL_DATABASE_URL", database_url)

    from app.config import get_settings
    import manage

    get_settings.cache_clear()
    manage.create_admin(
        Namespace(
            username="first-admin",
            full_name="Primer Administrador",
            password="secure-admin-password",
        )
    )

    with Session(create_engine(database_url)) as db:
        user = db.scalar(select(User).where(User.username == "first-admin"))
        assert user is not None
        assert user.role.role_name == "ADMIN"
        assert verify_password("secure-admin-password", user.password_hash)
    get_settings.cache_clear()
