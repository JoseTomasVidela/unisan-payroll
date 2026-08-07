from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.models import PayrollConceptRate, PayrollCycle
from conftest import login
from test_settlements import seed_settlement


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def create_and_apply(client, headers, cycle_id, percentage):
    created = client.post(
        "/api/rates/ipc-adjustments",
        headers=headers,
        json={
            "percentage": str(percentage),
            "effective_from_cycle_id": cycle_id,
        },
    )
    assert created.status_code == 201
    applied = client.post(
        f"/api/rates/ipc-adjustments/{created.json()['id']}/apply",
        headers=headers,
    )
    assert applied.status_code == 200
    return applied.json()


def test_ipc_applies_from_selected_cycle_and_can_restore_historical_prices(client, db_factory):
    seed_settlement(db_factory)
    with db_factory() as db:
        july = PayrollCycle(
            cycle_name="Ciclo Julio 2026",
            start_date=date(2026, 7, 1),
            end_date=date(2026, 7, 15),
        )
        db.add(july)
        db.commit()
        july_id = july.id

    headers = admin_headers(client)
    first = create_and_apply(client, headers, july_id, "10")
    assert first["effective_from_cycle_name"] == "Ciclo Julio 2026"

    with db_factory() as db:
        rates = list(db.scalars(select(PayrollConceptRate).order_by(PayrollConceptRate.id)).all())
        assert any(rate.effective_to_cycle_id == 1 and rate.amount == Decimal("5") for rate in rates)
        assert any(rate.effective_from_cycle_id == july_id and rate.amount == Decimal("5.5") for rate in rates)

    create_and_apply(client, headers, july_id, "20")
    restored = client.post(
        f"/api/rates/ipc-adjustments/{first['id']}/apply",
        headers=headers,
    )
    assert restored.status_code == 200

    with db_factory() as db:
        rates = list(db.scalars(select(PayrollConceptRate).where(PayrollConceptRate.active.is_(True))).all())
        assert any(rate.effective_from_cycle_id == july_id and rate.amount == Decimal("5.5") for rate in rates)
        assert not any(rate.effective_from_cycle_id == july_id and rate.amount == Decimal("6.6") for rate in rates)

