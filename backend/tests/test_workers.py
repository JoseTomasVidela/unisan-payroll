from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.models import Employee, PayrollConcept, PayrollConceptRate, PayrollImport, PayrollRecord, User
from conftest import login


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def user_headers(client):
    token = login(client, "consulta", "consulta-password")
    return {"Authorization": f"Bearer {token}"}


def test_workers_list_groups_same_name_and_admin_can_update_contract(client, db_factory):
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
        }
    ]

    worker_id = listed.json()[0]["id"]
    updated = client.put(
        f"/api/workers/{worker_id}",
        headers=admin_headers(client),
        json={"contract_type": "OLD"},
    )
    assert updated.status_code == 200
    with db_factory() as db:
        employees = db.scalars(
            select(Employee).where(Employee.employee_name == "Alejandro Escobar").order_by(Employee.id)
        ).all()
        assert [employee.contract_type for employee in employees] == ["OLD", "OLD"]


def test_user_cannot_edit_workers(client):
    response = client.post(
        "/api/workers",
        headers=user_headers(client),
        json={"employee_name": "Nuevo Trabajador", "contract_type": "NEW"},
    )
    assert response.status_code == 403


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
