from __future__ import annotations

from conftest import login
from test_settlements import seed_settlement


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def test_email_options_use_fixed_recipients_and_their_respective_pdfs(
    client, db_factory, monkeypatch
):
    driver_id, _ = seed_settlement(db_factory)
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
    assert deliveries[1]["recipient"] == "rrhh@unisan.cl"
    assert not deliveries[1]["pdf_file_name"].startswith("Planilla-")
    assert deliveries[1]["pdf_content"].startswith(b"%PDF-")
    assert deliveries[1]["subject"] == "Planilla de Liquidación - Chofer Uno - MAYO/2026"
    assert deliveries[1]["body"] == "Respaldo de producción Chofer Uno correspondiente a MAYO/2026"
