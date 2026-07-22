from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
from sqlalchemy import create_engine

from app.config import Settings
from app.database import (
    REQUIRED_PRODUCTION_TABLES,
    validate_database_url,
    validate_required_tables,
)
from app.main import bootstrap


def production_settings(database_url: str) -> Settings:
    return Settings(
        database_url=database_url,
        db_ssl_ca=None,
        jwt_secret="test-secret-with-at-least-32-characters",
        access_token_minutes=10,
        bootstrap_admin_username="admin",
        bootstrap_admin_password="admin-password",
        bootstrap_admin_name="Administrador",
        cors_origins=(),
    )


def test_mysql_url_must_point_to_unisan_db():
    with pytest.raises(RuntimeError, match="/unisan_db"):
        validate_database_url(
            "mysql+pymysql://user:password@server.mysql.database.azure.com/other_db"
        )


def test_mysql_url_accepts_unisan_db():
    validate_database_url(
        "mysql+pymysql://user:password@server.mysql.database.azure.com/unisan_db"
    )


def test_production_table_validation_reports_missing_tables():
    target_engine = create_engine("sqlite://")

    with pytest.raises(RuntimeError, match="payroll_users"):
        validate_required_tables(target_engine)


def test_production_bootstrap_validates_tables_and_syncs_permissions():
    settings = production_settings(
        "mysql+pymysql://user:password@server.mysql.database.azure.com/unisan_db"
    )
    target_engine = Mock()

    with patch("app.main.validate_required_tables") as validate_tables:
        with patch("app.main.Base.metadata.create_all") as create_all:
            with patch("app.main.PayrollHoliday.__table__.create") as create_holidays:
                with patch("app.main.Session") as session_factory:
                    with patch("app.main.seed_roles_and_permissions") as seed:
                        bootstrap(settings=settings, target_engine=target_engine)

    validate_tables.assert_called_once_with(target_engine)
    create_holidays.assert_called_once_with(bind=target_engine, checkfirst=True)
    create_all.assert_not_called()
    session_factory.assert_called_once_with(target_engine)
    seed.assert_called_once_with(session_factory.return_value.__enter__.return_value)


def test_sqlite_bootstrap_creates_local_tables():
    settings = production_settings("sqlite://")
    target_engine = create_engine("sqlite://")

    bootstrap(settings=settings, target_engine=target_engine)

    validate_required_tables(
        target_engine,
        frozenset(
            {
                "payroll_roles",
                "payroll_permissions",
                "payroll_role_permissions",
                "payroll_users",
            }
        ),
    )


def test_required_production_tables_are_all_payroll_prefixed():
    assert REQUIRED_PRODUCTION_TABLES
    assert all(name.startswith("payroll_") for name in REQUIRED_PRODUCTION_TABLES)


def test_required_production_tables_include_cell_overrides():
    assert "payroll_cell_overrides" in REQUIRED_PRODUCTION_TABLES
