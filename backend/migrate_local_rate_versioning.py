from __future__ import annotations

from sqlalchemy import inspect, text

from app import models  # noqa: F401 - registers all model tables in Base.metadata
from app.database import Base, build_engine, is_sqlite_url


def main() -> None:
    engine = build_engine()
    if not is_sqlite_url(str(engine.url)):
        raise SystemExit("Esta migracion controlada solo puede ejecutarse en SQLite local.")

    columns = {
        column["name"]
        for column in inspect(engine).get_columns("payroll_concept_rates")
    }
    definitions = {
        "effective_from_cycle_id": "INTEGER NULL REFERENCES payroll_cycles(id)",
        "effective_to_cycle_id": "INTEGER NULL REFERENCES payroll_cycles(id)",
        "created_by": "INTEGER NULL REFERENCES payroll_users(id)",
        "updated_at": "DATETIME NULL",
    }
    with engine.begin() as connection:
        for name, definition in definitions.items():
            if name not in columns:
                connection.execute(
                    text(f"ALTER TABLE payroll_concept_rates ADD COLUMN {name} {definition}")
                )
    Base.metadata.create_all(engine, tables=[Base.metadata.tables["payroll_audit_log"]])
    print("Versionado de tarifas alineado en SQLite local.")


if __name__ == "__main__":
    main()
