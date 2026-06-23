from sqlalchemy import func, select

from app.models import PayrollConcept, PayrollConceptRate
from seed_payroll_concepts import SEED_ITEMS, apply_base_concepts


def test_base_concepts_seed_creates_catalog_without_rates(db_factory):
    with db_factory() as db:
        apply_base_concepts(db)
        assert db.scalar(select(func.count(PayrollConcept.id))) == len(SEED_ITEMS)
        assert db.scalar(select(func.count(PayrollConceptRate.id))) == 0
        contexts = set(
            db.execute(
                select(
                    PayrollConcept.cost_center,
                    PayrollConcept.role_type,
                ).distinct()
            ).all()
        )
        assert contexts == {
            ("DR", "DRIVER"),
            ("DR", "ASSISTANT"),
            ("SERVICES", "DRIVER"),
            ("SERVICES", "ASSISTANT"),
        }


def test_base_concepts_seed_is_idempotent(db_factory):
    with db_factory() as db:
        apply_base_concepts(db)
        apply_base_concepts(db)
        assert db.scalar(select(func.count(PayrollConcept.id))) == len(SEED_ITEMS)


def test_services_week_2_concepts_are_present(db_factory):
    with db_factory() as db:
        apply_base_concepts(db)
        pairs = {
            (item.concept_code, item.cost_center, item.role_type)
            for item in db.scalars(select(PayrollConcept)).all()
        }
        assert ("SATURDAY_WEEK_2", "SERVICES", "DRIVER") in pairs
        assert ("SUNDAY_WEEK_2", "SERVICES", "DRIVER") in pairs
        assert ("SATURDAY_WEEK_2", "SERVICES", "ASSISTANT") in pairs
        assert ("SUNDAY_WEEK_2", "SERVICES", "ASSISTANT") in pairs
