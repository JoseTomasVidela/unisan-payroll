from sqlalchemy import select

from app.models import PayrollAuditLog, PayrollSetting, Role
from app.services import create_user
from conftest import login


def headers(client, username, password):
    token = login(client, username, password)
    return {"Authorization": f"Bearer {token}"}


def seed_operativo(db_factory):
    with db_factory() as db:
        create_user(
            db,
            username="operativo",
            full_name="Usuario Operativo",
            password="Operativo-1!",
            role_name="OPERATIVO",
        )


def test_admin_and_rrhh_can_control_operations_edit_lock(client, db_factory):
    initial = client.get(
        "/api/settings/operations-edit-lock",
        headers=headers(client, "admin", "admin-password"),
    )
    assert initial.status_code == 200
    assert initial.json()["locked"] is False
    assert initial.json()["can_control"] is True

    locked = client.put(
        "/api/settings/operations-edit-lock",
        headers=headers(client, "consulta", "consulta-password"),
        json={"locked": True},
    )
    assert locked.status_code == 200
    assert locked.json()["locked"] is True
    assert locked.json()["can_control"] is True
    assert locked.json()["updated_by"] == "Usuario RRHH"

    unlocked = client.put(
        "/api/settings/operations-edit-lock",
        headers=headers(client, "admin", "admin-password"),
        json={"locked": False},
    )
    assert unlocked.status_code == 200
    assert unlocked.json()["locked"] is False
    with db_factory() as db:
        setting = db.scalar(
            select(PayrollSetting).where(
                PayrollSetting.setting_key == "operations_edit_locked"
            )
        )
        assert setting.setting_value == "false"
        audits = db.scalars(
            select(PayrollAuditLog).where(
                PayrollAuditLog.action_type == "UPDATE_OPERATIONS_EDIT_LOCK"
            )
        ).all()
        assert len(audits) == 2


def test_admin_role_check_is_case_and_whitespace_tolerant(client, db_factory):
    with db_factory() as db:
        admin_role = db.scalar(select(Role).where(Role.role_name == "ADMIN"))
        admin_role.role_name = " Admin "
        db.commit()
    response = client.put(
        "/api/settings/operations-edit-lock",
        headers=headers(client, "admin", "admin-password"),
        json={"locked": True},
    )
    assert response.status_code == 200
    assert response.json()["locked"] is True
    assert response.json()["can_control"] is True


def test_lock_blocks_operativo_backend_edits_until_unlocked(client, db_factory):
    seed_operativo(db_factory)
    admin_headers = headers(client, "admin", "admin-password")
    operativo_headers = headers(client, "operativo", "Operativo-1!")

    operativo_state = client.get(
        "/api/settings/operations-edit-lock",
        headers=operativo_headers,
    )
    assert operativo_state.status_code == 200
    assert operativo_state.json()["can_control"] is False

    activities = client.get(
        "/api/settlements/activities?cost_center=DR&role_type=DRIVER&cycle_id=1",
        headers=operativo_headers,
    )
    assert activities.status_code == 200

    assert client.put(
        "/api/settings/operations-edit-lock",
        headers=admin_headers,
        json={"locked": True},
    ).status_code == 200

    blocked = client.post(
        "/api/settlements/cells",
        headers=operativo_headers,
        json={
            "cycle_id": 1,
            "employee_id": 999,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [
                {"concept_id": 1, "work_date": "2026-05-22", "value": "1"}
            ],
        },
    )
    assert blocked.status_code == 403
    assert "bloqueadas" in blocked.json()["detail"]
    blocked_activities = client.get(
        "/api/settlements/activities?cost_center=DR&role_type=DRIVER&cycle_id=1",
        headers=operativo_headers,
    )
    assert blocked_activities.status_code == 403

    rrhh_blocked = client.post(
        "/api/settlements/cells",
        headers=headers(client, "consulta", "consulta-password"),
        json={
            "cycle_id": 1,
            "employee_id": 999,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [
                {"concept_id": 1, "work_date": "2026-05-22", "value": "1"}
            ],
        },
    )
    assert rrhh_blocked.status_code == 403

    admin_blocked = client.post(
        "/api/settlements/cells",
        headers=admin_headers,
        json={
            "cycle_id": 1,
            "employee_id": 999,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [
                {"concept_id": 1, "work_date": "2026-05-22", "value": "1"}
            ],
        },
    )
    assert admin_blocked.status_code == 403

    cannot_control = client.put(
        "/api/settings/operations-edit-lock",
        headers=operativo_headers,
        json={"locked": False},
    )
    assert cannot_control.status_code == 403

    assert client.put(
        "/api/settings/operations-edit-lock",
        headers=admin_headers,
        json={"locked": False},
    ).status_code == 200
    allowed_through_permission = client.post(
        "/api/settlements/cells",
        headers=operativo_headers,
        json={
            "cycle_id": 1,
            "employee_id": 999,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [
                {"concept_id": 1, "work_date": "2026-05-22", "value": "1"}
            ],
        },
    )
    assert allowed_through_permission.status_code == 404
