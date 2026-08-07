from __future__ import annotations

from sqlalchemy import inspect

from app.models import PayrollSoftlandCode, PayrollSoftlandConceptMapping


def test_softland_models_use_payroll_prefixed_tables():
    assert PayrollSoftlandCode.__tablename__ == "payroll_softland_codes"
    assert (
        PayrollSoftlandConceptMapping.__tablename__
        == "payroll_softland_concept_mappings"
    )


def test_softland_mapping_has_foreign_keys_to_catalog_and_payroll_concepts():
    foreign_keys = {
        (foreign_key.parent.name, foreign_key.column.table.name)
        for foreign_key in PayrollSoftlandConceptMapping.__table__.foreign_keys
    }

    assert ("concept_id", "payroll_concepts") in foreign_keys
    assert ("softland_code", "payroll_softland_codes") in foreign_keys


def test_softland_mapping_keys_and_concepts_are_unique():
    table = PayrollSoftlandConceptMapping.__table__
    unique_column_sets = {
        tuple(column.name for column in constraint.columns)
        for constraint in table.constraints
        if constraint.__class__.__name__ == "UniqueConstraint"
    }

    assert ("mapping_type", "mapping_key") in unique_column_sets
    assert ("concept_id",) in unique_column_sets


def test_sqlite_bootstrap_creates_softland_mapping_schema(db_factory):
    inspector = inspect(db_factory.kw["bind"])

    assert "payroll_softland_codes" in inspector.get_table_names()
    assert "payroll_softland_concept_mappings" in inspector.get_table_names()
