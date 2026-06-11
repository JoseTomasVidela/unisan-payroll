from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.models import (
    Employee,
    PayrollConcept,
    PayrollConceptRate,
    PayrollCycle,
    PayrollImport,
    PayrollRecord,
    User,
)
from conftest import login


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def user_headers(client):
    token = login(client, "consulta", "consulta-password")
    return {"Authorization": f"Bearer {token}"}


def seed_rates_context(db_factory):
    with db_factory() as db:
        admin = db.scalar(select(User).where(User.username == "admin"))
        db.add_all(
            [
                PayrollCycle(
                    id=2,
                    cycle_name="Ciclo Julio 2026",
                    start_date=date(2026, 6, 22),
                    end_date=date(2026, 7, 21),
                ),
                PayrollCycle(
                    id=3,
                    cycle_name="Ciclo Agosto 2026",
                    start_date=date(2026, 7, 22),
                    end_date=date(2026, 8, 21),
                ),
            ]
        )
        worker = Employee(employee_name="Chofer Uno", role_type="DRIVER")
        db.add(worker)
        db.flush()
        payroll_import = PayrollImport(
            cycle_id=1,
            source_type="DR",
            cost_center="DR",
            file_name="seed.xlsx",
            imported_by=admin.id,
            rows_imported=3,
        )
        db.add(payroll_import)
        db.flush()
        concept = PayrollConcept(
            concept_code="EVENT",
            concept_name="Evento",
            db_field="event_flag",
            source_type="DR",
            cost_center="DR",
            role_type="DRIVER",
            display_order=1,
        )
        db.add(concept)
        db.flush()
        db.add_all(
            [
                PayrollConceptRate(
                    concept_id=concept.id,
                    amount=Decimal("5.0000"),
                    effective_from_cycle_id=1,
                    created_by=admin.id,
                ),
                PayrollRecord(
                    cycle_id=1,
                    import_id=payroll_import.id,
                    employee_id=worker.id,
                    source_type="DR",
                    cost_center="DR",
                    role_type="DRIVER",
                    source_employee_name=worker.employee_name,
                    source_row_number=2,
                    source_row_hash="a" * 64,
                    source_person_slot="OPERATOR",
                    work_date=date(2026, 5, 22),
                    event_flag=Decimal("2"),
                ),
            ]
        )
        db.commit()
        return worker.id, concept.id


def test_get_rates_returns_context_rows(client, db_factory):
    _, concept_id = seed_rates_context(db_factory)

    response = client.get(
        "/api/rates?cost_center=DR&role_type=DRIVER&cycle_id=1",
        headers=admin_headers(client),
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["concept_id"] == concept_id
    assert Decimal(body[0]["amount"]) == Decimal("5")


def test_admin_can_edit_rate_from_cycle_forward(client, db_factory):
    _, concept_id = seed_rates_context(db_factory)

    response = client.post(
        "/api/rates",
        headers=admin_headers(client),
        json={
            "concept_id": concept_id,
            "cycle_id": 2,
            "amount": "7.5000",
            "apply_mode": "FROM_CYCLE_FORWARD",
        },
    )

    assert response.status_code == 201
    with db_factory() as db:
        rates = db.scalars(
            select(PayrollConceptRate)
            .where(PayrollConceptRate.concept_id == concept_id)
            .order_by(PayrollConceptRate.id)
        ).all()
        assert [rate.amount for rate in rates if rate.active] == [Decimal("5"), Decimal("7.5")]
        assert rates[0].effective_to_cycle_id == 1
        assert rates[-1].effective_from_cycle_id == 2
        assert rates[-1].effective_to_cycle_id is None


def test_user_cannot_edit_rate(client, db_factory):
    _, concept_id = seed_rates_context(db_factory)

    response = client.post(
        "/api/rates",
        headers=user_headers(client),
        json={
            "concept_id": concept_id,
            "cycle_id": 2,
            "amount": "7.5000",
            "apply_mode": "FROM_CYCLE_FORWARD",
        },
    )

    assert response.status_code == 403


def test_single_cycle_rate_only_affects_selected_cycle(client, db_factory):
    _, concept_id = seed_rates_context(db_factory)

    response = client.post(
        "/api/rates",
        headers=admin_headers(client),
        json={
            "concept_id": concept_id,
            "cycle_id": 2,
            "amount": "9.0000",
            "apply_mode": "SINGLE_CYCLE",
        },
    )

    assert response.status_code == 201
    july = client.get(
        "/api/rates?cost_center=DR&role_type=DRIVER&cycle_id=2",
        headers=admin_headers(client),
    )
    august = client.get(
        "/api/rates?cost_center=DR&role_type=DRIVER&cycle_id=3",
        headers=admin_headers(client),
    )
    assert Decimal(july.json()[0]["amount"]) == Decimal("9")
    assert Decimal(august.json()[0]["amount"]) == Decimal("5")


def test_put_rate_updates_single_cycle_and_settlement_uses_effective_rate(client, db_factory):
    worker_id, concept_id = seed_rates_context(db_factory)
    create = client.post(
        "/api/rates",
        headers=admin_headers(client),
        json={
            "concept_id": concept_id,
            "cycle_id": 2,
            "amount": "8.0000",
            "apply_mode": "SINGLE_CYCLE",
        },
    )
    rate_id = create.json()["rate_id"]
    update = client.put(
        f"/api/rates/{rate_id}",
        headers=admin_headers(client),
        json={
            "cycle_id": 2,
            "amount": "12.0000",
            "apply_mode": "SINGLE_CYCLE",
        },
    )

    assert update.status_code == 200
    response = client.get(
        (
            f"/api/settlements?cycle_id=1&employee_id={worker_id}"
            "&cost_center=DR&role_type=DRIVER"
        ),
        headers=admin_headers(client),
    )
    assert response.status_code == 200
    assert Decimal(response.json()["rows"][0]["rate"]) == Decimal("5")
    july = client.get(
        "/api/rates?cost_center=DR&role_type=DRIVER&cycle_id=2",
        headers=admin_headers(client),
    )
    assert Decimal(july.json()[0]["amount"]) == Decimal("12")
