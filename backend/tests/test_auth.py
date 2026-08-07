from datetime import date

from conftest import login


def test_health_checks_database(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}


def test_login_returns_role_and_permissions(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin-password"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["role"] == "ADMIN"
    assert "users.manage" in body["user"]["permissions"]


def test_login_rejects_invalid_password(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "incorrecta"},
    )

    assert response.status_code == 401


def test_me_requires_token(client):
    assert client.get("/api/auth/me").status_code == 401


def test_rrhh_role_cannot_manage_users(client):
    token = login(client, "consulta", "consulta-password")

    response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_admin_can_create_user(client):
    token = login(client, "admin", "admin-password")

    response = client.post(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "nuevo",
            "full_name": "Nuevo Usuario",
            "password": "Nuevo-password!",
            "role_name": "OPERATIVO",
        },
    )

    assert response.status_code == 201
    assert response.json()["permissions"] == [
        "payroll.edit", "payroll.export", "payroll.import", "payroll.read"
    ]


def test_admin_can_list_roles_and_permissions(client):
    token = login(client, "admin", "admin-password")
    headers = {"Authorization": f"Bearer {token}"}

    roles = client.get("/api/roles", headers=headers)
    permissions = client.get("/api/permissions", headers=headers)

    assert roles.status_code == 200
    assert {role["role_name"] for role in roles.json()} == {"ADMIN", "OPERATIVO", "RRHH"}
    assert permissions.status_code == 200
    assert "users.manage" in {
        permission["permission_code"] for permission in permissions.json()
    }


def test_admin_can_reset_any_user_password(client):
    admin_token = login(client, "admin", "admin-password")
    users = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    target = next(user for user in users if user["username"] == "consulta")

    response = client.patch(
        f"/api/users/{target['id']}/password",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"password": "Nueva-clave!"},
    )

    assert response.status_code == 200
    assert login(client, "consulta", "Nueva-clave!")


def test_admin_can_reset_own_password(client):
    admin_token = login(client, "admin", "admin-password")
    users = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    target = next(user for user in users if user["username"] == "admin")

    response = client.patch(
        f"/api/users/{target['id']}/password",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"password": "Admin-nueva!"},
    )

    assert response.status_code == 200
    assert login(client, "admin", "Admin-nueva!")


def test_rrhh_cannot_reset_password(client):
    token = login(client, "consulta", "consulta-password")

    response = client.patch(
        "/api/users/1/password",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "Nueva-clave!"},
    )

    assert response.status_code == 403


def test_admin_can_edit_and_delete_user(client):
    token = login(client, "admin", "admin-password")
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post(
        "/api/users",
        headers=headers,
        json={
            "username": "editable",
            "full_name": "Usuario Editable",
            "password": "Clave-inicial!",
            "role_name": "OPERATIVO",
        },
    ).json()

    updated = client.patch(
        f"/api/users/{created['id']}",
        headers=headers,
        json={
            "username": "editado",
            "full_name": "Usuario Modificado",
            "role_name": "RRHH",
            "active": False,
        },
    )

    assert updated.status_code == 200
    assert updated.json()["username"] == "editado"
    assert updated.json()["full_name"] == "Usuario Modificado"
    assert updated.json()["role"] == "RRHH"
    assert updated.json()["active"] is False

    deleted = client.delete(f"/api/users/{created['id']}", headers=headers)
    assert deleted.status_code == 204
    assert created["id"] not in {
        user["id"] for user in client.get("/api/users", headers=headers).json()
    }


def test_admin_cannot_delete_self(client):
    token = login(client, "admin", "admin-password")
    headers = {"Authorization": f"Bearer {token}"}
    admin = next(
        user for user in client.get("/api/users", headers=headers).json()
        if user["username"] == "admin"
    )

    response = client.delete(f"/api/users/{admin['id']}", headers=headers)

    assert response.status_code == 400


def test_audit_is_admin_only_and_lists_actions_for_date(client):
    admin_token = login(client, "admin", "admin-password")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    client.post(
        "/api/users",
        headers=admin_headers,
        json={
            "username": "auditado",
            "full_name": "Usuario Auditado",
            "password": "Clave-auditada!",
            "role_name": "OPERATIVO",
        },
    )

    chile_date = date.today().isoformat()
    response = client.get(
        f"/api/audit?audit_date={chile_date}",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert any(
        item["username"] == "admin" and "Agregó un usuario" in item["action"]
        for item in response.json()
    )

    rrhh_token = login(client, "consulta", "consulta-password")
    forbidden = client.get(
        f"/api/audit?audit_date={chile_date}",
        headers={"Authorization": f"Bearer {rrhh_token}"},
    )
    assert forbidden.status_code == 403

    exported = client.get(
        f"/api/audit/export?audit_date={chile_date}",
        headers=admin_headers,
    )
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/pdf"
    assert exported.content.startswith(b"%PDF-1.4")
