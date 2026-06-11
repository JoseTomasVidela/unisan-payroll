from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("PAYROLL_DATABASE_URL", "sqlite://")
os.environ.setdefault("PAYROLL_JWT_SECRET", "test-secret-with-at-least-32-characters")

from app.config import Settings, get_settings
from app.database import Base, get_db
from app.main import app
from app.models import PayrollCycle
from app.services import create_user, seed_roles_and_permissions


@pytest.fixture
def db_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as db:
        seed_roles_and_permissions(db)
        db.add(
            PayrollCycle(
                id=1,
                cycle_name="Ciclo Junio 2026",
                start_date=date(2026, 5, 22),
                end_date=date(2026, 6, 21),
            )
        )
        db.commit()
        create_user(
            db,
            username="admin",
            full_name="Administrador",
            password="admin-password",
            role_name="ADMIN",
        )
        create_user(
            db,
            username="consulta",
            full_name="Usuario Consulta",
            password="consulta-password",
            role_name="USER",
        )
    return factory


@pytest.fixture
def client(db_factory):
    def override_db():
        with db_factory() as db:
            yield db

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_settings] = lambda: Settings(
        database_url="sqlite://",
        db_ssl_ca=None,
        jwt_secret="test-secret-with-at-least-32-characters",
        access_token_minutes=10,
        bootstrap_admin_username=None,
        bootstrap_admin_password=None,
        bootstrap_admin_name="Administrador",
        cors_origins=(),
    )
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def login(client: TestClient, username: str, password: str) -> str:
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
