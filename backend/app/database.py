from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import get_settings


class Base(DeclarativeBase):
    pass


REQUIRED_PRODUCTION_TABLES = frozenset(
    {
        "payroll_cycles",
        "payroll_roles",
        "payroll_permissions",
        "payroll_role_permissions",
        "payroll_users",
        "payroll_employees",
        "payroll_imports",
        "payroll_records",
        "payroll_concepts",
        "payroll_concept_rates",
        "payroll_manual_adjustments",
        "payroll_cell_overrides",
        "payroll_audit_log",
        "payroll_export_logs",
    }
)

REQUIRED_TABLE_COLUMNS = {
    "payroll_users": frozenset(
        {
            "username",
            "full_name",
            "password_hash",
            "role_id",
            "active",
            "created_at",
            "last_login_at",
        }
    ),
    "payroll_employees": frozenset(
        {
            "employee_name",
            "role_type",
            "contract_type",
        }
    ),
    "payroll_imports": frozenset(
        {
            "cycle_id",
            "source_type",
            "cost_center",
            "file_name",
            "imported_by",
            "rows_imported",
            "imported_at",
        }
    ),
    "payroll_records": frozenset(
        {
            "cycle_id",
            "import_id",
            "employee_id",
            "source_type",
            "cost_center",
            "role_type",
            "source_employee_name",
            "source_employee_code",
            "source_row_number",
            "source_row_hash",
            "source_person_slot",
            "work_date",
            "duration_minutes",
            "status",
            "dispatch_flag",
            "entry_before_1930_qty",
            "entry_before_0730_qty",
            "exit_after_1930_qty",
            "fair_week_1_flag",
            "fair_week_2_flag",
            "outside_radius_flag",
            "outside_radius_v_region_qty",
            "saturday_week_1_qty",
            "sunday_week_1_qty",
            "saturday_week_2_qty",
            "sunday_week_2_qty",
            "client_trips_qty",
            "saturday_after_1600_qty",
            "sunday_after_1600_qty",
            "cleaning_flag",
            "drying_flag",
            "weekend_cleaning_qty",
            "weekend_drying_qty",
            "event_flag",
            "water_point_flag",
            "kit_delivery_flag",
            "lavatory_load_flag",
            "large_trash_bin_qty",
            "small_trash_bin_qty",
            "fosa_qty",
            "riles_suction_flag",
        }
    ),
    "payroll_concepts": frozenset(
        {
            "concept_code",
            "concept_name",
            "db_field",
            "source_type",
            "cost_center",
            "role_type",
            "display_order",
            "active",
            "created_at",
        }
    ),
    "payroll_concept_rates": frozenset(
        {
            "concept_id",
            "amount",
            "contract_type",
            "effective_from_cycle_id",
            "effective_to_cycle_id",
            "created_by",
            "active",
            "created_at",
            "updated_at",
        }
    ),
    "payroll_manual_adjustments": frozenset(
        {
            "cycle_id",
            "employee_id",
            "cost_center",
            "role_type",
            "adjustment_type",
            "adjustment_name",
            "adjustment_date",
            "units",
            "amount",
            "notes",
            "active",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "deleted_at",
        }
    ),
    "payroll_cell_overrides": frozenset(
        {
            "cycle_id",
            "employee_id",
            "concept_id",
            "cost_center",
            "role_type",
            "work_date",
            "override_value",
            "created_by",
            "created_at",
            "updated_at",
        }
    ),
}


def is_sqlite_url(database_url: str) -> bool:
    return make_url(database_url).get_backend_name() == "sqlite"


def validate_database_url(database_url: str) -> None:
    url = make_url(database_url)
    backend = url.get_backend_name()
    if backend == "sqlite":
        return
    if backend != "mysql":
        raise RuntimeError("PAYROLL_DATABASE_URL debe utilizar SQLite local o MySQL.")
    if url.database != "unisan_db":
        raise RuntimeError(
            "PAYROLL_DATABASE_URL de MySQL debe apuntar explícitamente a /unisan_db."
        )


def build_engine(database_url: str | None = None) -> Engine:
    settings = get_settings()
    url = database_url or settings.database_url
    validate_database_url(url)
    connect_args: dict[str, object] = {}

    if is_sqlite_url(url):
        connect_args["check_same_thread"] = False
    elif settings.db_ssl_ca:
        connect_args["ssl"] = {"ca": settings.db_ssl_ca}

    return create_engine(url, pool_pre_ping=True, connect_args=connect_args)


engine = build_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def check_connection(db: Session) -> None:
    db.execute(text("SELECT 1"))


def validate_required_tables(
    target_engine: Engine,
    required_tables: frozenset[str] = REQUIRED_PRODUCTION_TABLES,
) -> None:
    inspector = inspect(target_engine)
    existing_tables = set(inspector.get_table_names())
    missing_tables = sorted(required_tables - existing_tables)
    if missing_tables:
        raise RuntimeError(
            "Faltan tablas requeridas en unisan_db: " + ", ".join(missing_tables)
        )
    for table_name, required_columns in REQUIRED_TABLE_COLUMNS.items():
        existing_columns = {
            column["name"] for column in inspector.get_columns(table_name)
        }
        missing_columns = sorted(required_columns - existing_columns)
        if missing_columns:
            raise RuntimeError(
                f"Faltan columnas requeridas en {table_name}: "
                + ", ".join(missing_columns)
            )
