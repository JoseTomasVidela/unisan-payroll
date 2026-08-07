from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select

from app.models import PayrollAuditLog, PayrollManualAdjustment
from conftest import login
from test_settlements import seed_settlement


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def user_headers(client):
    token = login(client, "consulta", "consulta-password")
    return {"Authorization": f"Bearer {token}"}


def test_admin_can_create_manual_adjustment_and_recalculate_production_total(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    created = client.post(
        "/api/manual-adjustments",
        headers=admin_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "Bono puntual",
            "units": "2",
            "amount": "12.5",
            "observations": "Aprobado por finanzas",
        },
    )

    assert created.status_code == 201
    body = created.json()
    assert body["adjustment_type"] == "PRODUCTION_BONUS"
    assert body["description"] == "Bono puntual"
    assert Decimal(body["amount"]) == Decimal("12.5")
    assert body["active"] is True
    assert body["history"][0]["action_type"] == "CREATE_MANUAL_ADJUSTMENT"

    settlement = client.get(
        f"/api/liquidations?cycle_id=1&employee_id={driver_id}",
        headers=admin_headers(client),
    )
    assert settlement.status_code == 200
    assert Decimal(settlement.json()["production_total"]) == Decimal("112.5")
    adjustment_row = next(
        row for row in settlement.json()["rows"]
        if row["row_type"] == "adjustment_production_bonus"
    )
    assert adjustment_row["concept_name"] == "Bono puntual — Aprobado por finanzas"


def test_enabled_bonus_types_are_available(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    for adjustment_type, expected_name in (
        ("VACATION_BONUS", "Bono Vacaciones"),
        ("PRODUCTION_BONUS", "Bono Producción"),
        ("EVENT_BONUS", "Bono Evento"),
    ):
        created = client.post(
            "/api/manual-adjustments",
            headers=admin_headers(client),
            json={
                "cycle_id": 1,
                "employee_id": driver_id,
                "adjustment_type": adjustment_type,
                "description": None,
                "units": "1",
                "amount": "10",
                "observations": "Detalle visible",
            },
        )
        assert created.status_code == 201
        assert created.json()["description"] == expected_name

    settlement = client.get(
        f"/api/liquidations?cycle_id=1&employee_id={driver_id}",
        headers=admin_headers(client),
    )
    assert settlement.status_code == 200
    names = {row["concept_name"] for row in settlement.json()["rows"]}
    assert "Bono Producción — Detalle visible" in names
    assert "Bono Evento — Detalle visible" in names
    assert "Bono Vacaciones — Detalle visible" in names


def test_admin_can_create_manual_adjustment_without_description(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    created = client.post(
        "/api/manual-adjustments",
        headers=admin_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "adjustment_type": "VACATION_BONUS",
            "description": None,
            "units": "2",
            "amount": "20",
            "observations": "Sin descripcion manual",
        },
    )

    assert created.status_code == 201
    body = created.json()
    assert body["adjustment_type"] == "VACATION_BONUS"
    assert body["description"] == "Bono Vacaciones"
    assert Decimal(body["amount"]) == Decimal("20")


def test_admin_can_edit_manual_adjustment(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    created = client.post(
        "/api/manual-adjustments",
        headers=admin_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "Bono puntual",
            "units": "1",
            "amount": "10",
            "observations": "Inicial",
        },
    )
    adjustment_id = created.json()["id"]

    updated = client.put(
        f"/api/manual-adjustments/{adjustment_id}",
        headers=admin_headers(client),
        json={
            "adjustment_type": "VACATION_BONUS",
            "description": "Ajuste final",
            "units": "3",
            "amount": "17",
            "observations": "Corregido",
        },
    )

    assert updated.status_code == 200
    body = updated.json()
    assert body["adjustment_type"] == "VACATION_BONUS"
    assert body["description"] == "Ajuste final"
    assert Decimal(body["units"]) == Decimal("3")
    assert Decimal(body["amount"]) == Decimal("17")
    assert any(item["action_type"] == "UPDATE_MANUAL_ADJUSTMENT" for item in body["history"])


def test_admin_can_edit_manual_adjustment_without_description(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    created = client.post(
        "/api/manual-adjustments",
        headers=admin_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "Bono inicial",
            "units": "1",
            "amount": "10",
            "observations": "Inicial",
        },
    )
    adjustment_id = created.json()["id"]

    updated = client.put(
        f"/api/manual-adjustments/{adjustment_id}",
        headers=admin_headers(client),
        json={
            "adjustment_type": "VACATION_BONUS",
            "description": None,
            "units": "3",
            "amount": "17",
            "observations": "Corregido",
        },
    )

    assert updated.status_code == 200
    body = updated.json()
    assert body["adjustment_type"] == "VACATION_BONUS"
    assert body["description"] == "Bono Vacaciones"


def test_admin_can_soft_delete_manual_adjustment(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    created = client.post(
        "/api/manual-adjustments",
        headers=admin_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "Bono temporal",
            "units": None,
            "amount": "8",
            "observations": None,
        },
    )
    adjustment_id = created.json()["id"]

    deleted = client.delete(
        f"/api/manual-adjustments/{adjustment_id}",
        headers=admin_headers(client),
    )

    assert deleted.status_code == 200
    body = deleted.json()
    assert body["active"] is False
    assert body["deleted_at"] is not None
    assert any(item["action_type"] == "DELETE_MANUAL_ADJUSTMENT" for item in body["history"])

    listed = client.get(
        f"/api/manual-adjustments?cycle_id=1&employee_id={driver_id}",
        headers=admin_headers(client),
    )
    assert listed.status_code == 200
    assert listed.json() == []

    settlement = client.get(
        f"/api/liquidations?cycle_id=1&employee_id={driver_id}",
        headers=admin_headers(client),
    )
    assert settlement.status_code == 200
    assert Decimal(settlement.json()["production_total"]) == Decimal("87.5")


def test_user_cannot_create_edit_or_delete_manual_adjustments(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    created = client.post(
        "/api/manual-adjustments",
        headers=user_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "No autorizado",
            "units": None,
            "amount": "5",
            "observations": None,
        },
    )
    assert created.status_code == 403

    created = client.post(
        "/api/manual-adjustments",
        headers=admin_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "Autorizado",
            "units": None,
            "amount": "5",
            "observations": None,
        },
    )
    adjustment_id = created.json()["id"]

    updated = client.put(
        f"/api/manual-adjustments/{adjustment_id}",
        headers=user_headers(client),
        json={
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "Cambio no autorizado",
            "units": None,
            "amount": "7",
            "observations": None,
        },
    )
    deleted = client.delete(
        f"/api/manual-adjustments/{adjustment_id}",
        headers=user_headers(client),
    )

    assert updated.status_code == 403
    assert deleted.status_code == 403


def test_manual_adjustment_list_returns_history_and_audit_rows(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    created = client.post(
        "/api/manual-adjustments",
        headers=admin_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "Bono de prueba",
            "units": None,
            "amount": "9",
            "observations": "Semana 1",
        },
    )
    adjustment_id = created.json()["id"]
    client.put(
        f"/api/manual-adjustments/{adjustment_id}",
        headers=admin_headers(client),
        json={
            "adjustment_type": "PRODUCTION_BONUS",
            "description": "Bono actualizado",
            "units": None,
            "amount": "11",
            "observations": "Semana 1 ajustada",
        },
    )

    response = client.get(
        f"/api/manual-adjustments?cycle_id=1&employee_id={driver_id}",
        headers=admin_headers(client),
    )

    assert response.status_code == 200
    listed = response.json()
    assert len(listed) == 1
    assert listed[0]["description"] == "Bono actualizado"
    actions = [item["action_type"] for item in listed[0]["history"]]
    assert "CREATE_MANUAL_ADJUSTMENT" in actions
    assert "UPDATE_MANUAL_ADJUSTMENT" in actions


def test_adjustment_types_outside_enabled_adjustments_are_rejected(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    for adjustment_type in ("BONUS", "MANUAL_ADJUSTMENT", "DISCOUNT"):
        response = client.post(
            "/api/manual-adjustments",
            headers=admin_headers(client),
            json={
                "cycle_id": 1,
                "employee_id": driver_id,
                "adjustment_type": adjustment_type,
                "description": None,
                "units": None,
                "amount": "9",
                "observations": None,
            },
        )

        assert response.status_code == 422


