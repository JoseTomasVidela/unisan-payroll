from __future__ import annotations

from app.models import Employee
from conftest import login
from test_settlements import seed_settlement


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def test_sheet_keeps_fixed_recipient_and_settlement_uses_worker_email(
    client, db_factory, monkeypatch
):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        driver = db.get(Employee, driver_id)
        driver.email = "chofer.uno@example.com"
        db.commit()
    deliveries = []

    def capture_email(_settings, **kwargs):
        deliveries.append(kwargs)
        return kwargs["recipient"]

    monkeypatch.setattr("app.main.send_settlement_email", capture_email)

    for email_type in ("SHEET", "SETTLEMENT"):
        response = client.post(
            "/api/email/settlement",
            headers=admin_headers(client),
            json={
                "cycle_id": 1,
                "employee_id": driver_id,
                "cost_center": "DR",
                "role_type": "DRIVER",
                "email_type": email_type,
            },
        )
        assert response.status_code == 200

    assert deliveries[0]["recipient"] == "jose.videla@acsa-tec.cl"
    assert deliveries[0]["pdf_file_name"].startswith("Planilla-")
    assert deliveries[0]["pdf_content"].startswith(b"%PDF-")
    assert deliveries[0]["subject"] == "Planilla de Liquidación - Chofer Uno - MAYO/2026"
    assert deliveries[0]["body"] == "Respaldo de producción Chofer Uno correspondiente a MAYO/2026"
    assert b"Chofer Uno" in deliveries[0]["pdf_content"]
    assert b"Actividad" not in deliveries[0]["pdf_content"]
    assert deliveries[1]["recipient"] == "chofer.uno@example.com"
    assert deliveries[1]["recipient_name"] == "Chofer Uno"
    assert not deliveries[1]["pdf_file_name"].startswith("Planilla-")
    assert deliveries[1]["pdf_content"].startswith(b"%PDF-")
    assert deliveries[1]["subject"] == "Planilla de Liquidación - Chofer Uno - MAYO/2026"
    assert deliveries[1]["body"] == "Respaldo de producción Chofer Uno correspondiente a MAYO/2026"


def test_settlement_email_rejects_worker_without_registered_email(client, db_factory, monkeypatch):
    driver_id, _ = seed_settlement(db_factory)
    deliveries = []
    monkeypatch.setattr("app.main.send_settlement_email", lambda *_args, **kwargs: deliveries.append(kwargs))

    response = client.post(
        "/api/email/settlement",
        headers=admin_headers(client),
        json={"cycle_id": 1, "employee_id": driver_id, "email_type": "SETTLEMENT"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Trabajador Chofer Uno no tiene un correo registrado, por favor ingrese un correo "
        "válido en la sección de Trabajadores y vuelva a intentarlo."
    )
    assert deliveries == []


def test_batch_validates_all_workers_before_sending_any_email(client, db_factory, monkeypatch):
    driver_id, assistant_id = seed_settlement(db_factory)
    with db_factory() as db:
        db.get(Employee, driver_id).email = "chofer.uno@example.com"
        db.commit()
    deliveries = []
    monkeypatch.setattr("app.main.send_settlement_email", lambda *_args, **kwargs: deliveries.append(kwargs))

    response = client.post(
        "/api/email/settlements/batch",
        headers=admin_headers(client),
        json={"items": [
            {"cycle_id": 1, "employee_id": driver_id},
            {"cycle_id": 1, "employee_id": assistant_id},
        ]},
    )

    assert response.status_code == 400
    assert response.json()["detail"].startswith("Trabajador Auxiliar Uno no tiene un correo registrado")
    assert deliveries == []


def test_batch_sends_each_pdf_only_to_its_corresponding_worker(client, db_factory, monkeypatch):
    driver_id, assistant_id = seed_settlement(db_factory)
    with db_factory() as db:
        db.get(Employee, driver_id).email = "chofer.uno@example.com"
        db.get(Employee, assistant_id).email = "auxiliar.uno@example.com"
        db.commit()
    deliveries = []
    monkeypatch.setattr("app.main.send_settlement_email", lambda *_args, **kwargs: deliveries.append(kwargs))

    response = client.post(
        "/api/email/settlements/batch",
        headers=admin_headers(client),
        json={"items": [
            {"cycle_id": 1, "employee_id": driver_id},
            {"cycle_id": 1, "employee_id": assistant_id},
        ]},
    )

    assert response.status_code == 200
    assert response.json()["sent_count"] == 2
    assert [(item["recipient_name"], item["recipient"]) for item in deliveries] == [
        ("Chofer Uno", "chofer.uno@example.com"),
        ("Auxiliar Uno", "auxiliar.uno@example.com"),
    ]
    assert b"Chofer Uno" in deliveries[0]["pdf_content"]
    assert b"Auxiliar Uno" not in deliveries[0]["pdf_content"]
    assert b"Auxiliar Uno" in deliveries[1]["pdf_content"]
    assert b"Chofer Uno" not in deliveries[1]["pdf_content"]
