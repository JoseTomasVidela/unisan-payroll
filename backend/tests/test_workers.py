from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.employee_names import names_refer_to_same_person
from app.models import Employee, PayrollConcept, PayrollConceptRate, PayrollImport, PayrollRecord, User
from conftest import login


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def user_headers(client):
    token = login(client, "consulta", "consulta-password")
    return {"Authorization": f"Bearer {token}"}


def test_workers_list_groups_same_name_and_admin_can_update_contract_and_contact_data(client, db_factory):
    with db_factory() as db:
        db.add_all(
            [
                Employee(employee_name="Alejandro Escobar", role_type="DRIVER"),
                Employee(employee_name="Alejandro Escobar", role_type="ASSISTANT"),
            ]
        )
        db.commit()

    listed = client.get("/api/workers", headers=admin_headers(client))
    assert listed.status_code == 200
    assert listed.json() == [
        {
            "id": listed.json()[0]["id"],
            "employee_name": "Alejandro Escobar",
            "contract_type": None,
            "rut": None,
            "email": None,
            "cargo": None,
            "cost_center": None,
        }
    ]

    worker_id = listed.json()[0]["id"]
    updated = client.put(
        f"/api/workers/{worker_id}",
        headers=admin_headers(client),
        json={
            "contract_type": "OLD",
            "rut": "12.345.678-9",
            "email": "alejandro@unisan.cl",
            "cargo": "Chofer",
            "cost_center": "DR",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["rut"] == "12.345.678-9"
    assert updated.json()["email"] == "alejandro@unisan.cl"
    assert updated.json()["cargo"] == "Chofer"
    assert updated.json()["cost_center"] == "DR"
    with db_factory() as db:
        employees = db.scalars(
            select(Employee).where(Employee.employee_name == "Alejandro Escobar").order_by(Employee.id)
        ).all()
        assert [employee.contract_type for employee in employees] == ["OLD", "OLD"]
        assert [employee.rut for employee in employees] == ["12.345.678-9", "12.345.678-9"]
        assert [employee.email for employee in employees] == [
            "alejandro@unisan.cl",
            "alejandro@unisan.cl",
        ]
        assert [employee.cargo for employee in employees] == ["Chofer", "Chofer"]
        assert [employee.cost_center for employee in employees] == ["DR", "DR"]


def test_admin_can_create_worker_with_services_cost_center(client, db_factory):
    response = client.post(
        "/api/workers",
        headers=admin_headers(client),
        json={
            "employee_name": "Trabajador Servicios",
            "cost_center": "SERVICES",
            "contract_type": "NEW",
            "rut": "11.111.111-1",
            "email": "servicios@unisan.cl",
            "cargo": "Auxiliar",
        },
    )
    assert response.status_code == 201
    assert response.json()["cost_center"] == "SERVICES"
    with db_factory() as db:
        worker = db.scalar(
            select(Employee).where(Employee.employee_name == "Trabajador Servicios")
        )
        assert worker.cost_center == "SERVICES"


def test_create_worker_requires_valid_cost_center(client):
    missing = client.post(
        "/api/workers",
        headers=admin_headers(client),
        json={"employee_name": "Sin Centro"},
    )
    invalid = client.post(
        "/api/workers",
        headers=admin_headers(client),
        json={"employee_name": "Centro Invalido", "cost_center": "OTRO"},
    )
    assert missing.status_code == 422
    assert invalid.status_code == 400


def test_admin_can_create_cost_center_and_assign_it_to_worker(client):
    headers = admin_headers(client)
    created_center = client.post(
        "/api/settings/cost-centers",
        headers=headers,
        json={"name": "Operaciones Norte"},
    )
    assert created_center.status_code == 201
    assert created_center.json()["code"] == "OPERACIONES_NORTE"

    created_worker = client.post(
        "/api/workers",
        headers=headers,
        json={
            "employee_name": "Trabajador Norte",
            "cost_center": "OPERACIONES_NORTE",
        },
    )
    assert created_worker.status_code == 201
    assert created_worker.json()["cost_center"] == "OPERACIONES_NORTE"
    in_use_delete = client.delete(
        f"/api/settings/cost-centers/{created_center.json()['id']}",
        headers=headers,
    )
    assert in_use_delete.status_code == 409


def test_admin_can_create_adjustment_type_with_worked_day_value(client):
    response = client.post(
        "/api/settings/adjustment-types",
        headers=admin_headers(client),
        json={"name": "Capacitación", "worked_day_value": 1},
    )
    assert response.status_code == 201
    assert response.json()["code"] == "CAPACITACION"
    assert response.json()["worked_day_value"] == 1

    listed = client.get("/api/settings/adjustment-types", headers=admin_headers(client))
    assert listed.status_code == 200
    assert any(item["name"] == "Capacitación" for item in listed.json())
    updated = client.put(
        f"/api/settings/adjustment-types/{response.json()['id']}",
        headers=admin_headers(client),
        json={"worked_day_value": 0},
    )
    assert updated.status_code == 200
    assert updated.json()["worked_day_value"] == 0
    deleted = client.delete(
        f"/api/settings/adjustment-types/{response.json()['id']}",
        headers=admin_headers(client),
    )
    assert deleted.status_code == 204


def test_workers_list_prefers_full_name_when_available(client, db_factory):
    with db_factory() as db:
        db.add(
            Employee(
                employee_name="Alejandro Escobar",
                first_name="Alejandro",
                middle_name="Antonio",
                paternal_surname="Escobar",
                maternal_surname="Osorio",
                role_type="UNASSIGNED",
            )
        )
        db.commit()

    listed = client.get("/api/workers", headers=admin_headers(client))
    assert listed.status_code == 200
    assert listed.json()[0]["employee_name"] == "Alejandro Antonio Escobar Osorio"


def test_rrhh_can_create_workers(client):
    response = client.post(
        "/api/workers",
        headers=user_headers(client),
        json={
            "employee_name": "Nuevo Trabajador",
            "cost_center": "DR",
            "contract_type": "NEW",
            "rut": "11.111.111-1",
            "email": "nuevo@unisan.cl",
            "cargo": "Cargo prueba",
        },
    )
    assert response.status_code == 201
    assert response.json()["cost_center"] == "DR"


def test_admin_can_delete_worker_without_historical_records(client, db_factory):
    with db_factory() as db:
        worker = Employee(employee_name="Temporal Sin Uso", role_type="UNASSIGNED")
        db.add(worker)
        db.commit()
        worker_id = worker.id

    response = client.delete(f"/api/workers/{worker_id}", headers=admin_headers(client))
    assert response.status_code == 204

    with db_factory() as db:
        assert db.get(Employee, worker_id) is None


def test_workers_name_matching_accepts_surname_first_master_data(client, db_factory):
    assert names_refer_to_same_person(
        "Alejandro Escobar",
        "Escobar Osorio Alejandro Antonio",
    )


def test_settlement_prefers_contract_specific_rate_over_legacy_rate(client, db_factory):
    with db_factory() as db:
        admin = db.scalar(select(User).where(User.username == "admin"))
        worker = Employee(employee_name="Chofer Nuevo", role_type="DRIVER", contract_type="NEW")
        db.add(worker)
        db.flush()
        worker_id = worker.id
        payroll_import = PayrollImport(
            cycle_id=1,
            source_type="DR",
            cost_center="DR",
            file_name="seed.xlsx",
            imported_by=admin.id,
            rows_imported=1,
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
                    amount=Decimal("5"),
                    effective_from_cycle_id=1,
                    created_by=admin.id,
                ),
                PayrollConceptRate(
                    concept_id=concept.id,
                    contract_type="NEW",
                    amount=Decimal("9"),
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
                    source_row_hash="z" * 64,
                    source_person_slot="OPERATOR",
                    work_date=date(2026, 5, 22),
                    event_flag=Decimal("2"),
                ),
            ]
        )
        db.commit()

    response = client.get(
        f"/api/settlements?cycle_id=1&employee_id={worker_id}&cost_center=DR&role_type=DRIVER",
        headers=admin_headers(client),
    )
    assert response.status_code == 200
    first_row = response.json()["rows"][0]
    assert Decimal(first_row["rate"]) == Decimal("9")
    assert Decimal(first_row["total"]) == Decimal("18")
