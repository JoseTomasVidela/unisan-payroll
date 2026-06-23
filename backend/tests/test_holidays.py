from __future__ import annotations

from conftest import login


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def user_headers(client):
    token = login(client, "consulta", "consulta-password")
    return {"Authorization": f"Bearer {token}"}


def test_list_holidays_returns_default_chile_and_world_rows(client):
    response = client.get("/api/holidays?year=2026&month=12", headers=admin_headers(client))

    assert response.status_code == 200
    body = response.json()
    assert any(item["holiday_scope"] == "CHILE" and item["holiday_name"] == "Navidad" for item in body)
    assert any(item["holiday_scope"] == "WORLD" and item["holiday_name"] == "Christmas Day" for item in body)


def test_admin_can_create_and_update_custom_holiday(client):
    created = client.post(
        "/api/holidays",
        headers=admin_headers(client),
        json={
            "holiday_date": "2026-06-15",
            "holiday_name": "Feriado empresa",
            "holiday_scope": "CUSTOM",
            "active": True,
        },
    )

    assert created.status_code == 201
    holiday_id = created.json()["id"]

    updated = client.put(
        f"/api/holidays/{holiday_id}",
        headers=admin_headers(client),
        json={
            "holiday_date": "2026-06-16",
            "holiday_name": "Feriado empresa ajustado",
            "holiday_scope": "CUSTOM",
            "active": False,
        },
    )

    assert updated.status_code == 200
    body = updated.json()
    assert body["holiday_date"] == "2026-06-16"
    assert body["holiday_name"] == "Feriado empresa ajustado"
    assert body["active"] is False


def test_user_cannot_edit_holidays(client):
    response = client.post(
        "/api/holidays",
        headers=user_headers(client),
        json={
            "holiday_date": "2026-06-15",
            "holiday_name": "No autorizado",
            "holiday_scope": "CUSTOM",
            "active": True,
        },
    )

    assert response.status_code == 403
