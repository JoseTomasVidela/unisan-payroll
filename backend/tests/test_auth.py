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


def test_user_role_cannot_manage_users(client):
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
            "password": "nuevo-password",
            "role_name": "USER",
        },
    )

    assert response.status_code == 201
    assert response.json()["permissions"] == ["payroll.export", "payroll.read"]


def test_admin_can_list_roles_and_permissions(client):
    token = login(client, "admin", "admin-password")
    headers = {"Authorization": f"Bearer {token}"}

    roles = client.get("/api/roles", headers=headers)
    permissions = client.get("/api/permissions", headers=headers)

    assert roles.status_code == 200
    assert {role["role_name"] for role in roles.json()} == {"ADMIN", "USER"}
    assert permissions.status_code == 200
    assert "users.manage" in {
        permission["permission_code"] for permission in permissions.json()
    }
