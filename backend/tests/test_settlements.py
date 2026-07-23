from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import select

from app.models import (
    Employee,
    PayrollCellOverride,
    PayrollConcept,
    PayrollConceptRate,
    PayrollAuditLog,
    PayrollCycle,
    PayrollHoliday,
    PayrollManualAdjustment,
    PayrollImport,
    PayrollRecord,
    User,
)
from app.settlements import SettlementEngine
from conftest import login


def auth_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def seed_settlement(db_factory):
    with db_factory() as db:
        admin = db.scalar(select(User).where(User.username == "admin"))
        driver = Employee(employee_name="Chofer Uno", role_type="DRIVER")
        assistant = Employee(employee_name="Auxiliar Uno", role_type="ASSISTANT")
        db.add_all([driver, assistant])
        db.flush()
        payroll_import = PayrollImport(
            cycle_id=1,
            source_type="DR",
            cost_center="DR",
            file_name="seed.xlsx",
            imported_by=admin.id,
            rows_imported=3,
        )
        db.add(payroll_import)
        db.flush()
        event = PayrollConcept(
            concept_code="EVENT",
            concept_name="Evento",
            db_field="event_flag",
            source_type="DR",
            cost_center="DR",
            role_type="DRIVER",
            display_order=1,
        )
        dispatch = PayrollConcept(
            concept_code="DISPATCH_RETRIEVAL",
            concept_name="Despacho / Retiro",
            db_field="dispatch_flag",
            source_type="DR",
            cost_center="DR",
            role_type="DRIVER",
            display_order=2,
        )
        db.add_all([event, dispatch])
        db.flush()
        db.add_all(
            [
                PayrollConceptRate(
                    concept_id=event.id,
                    amount=Decimal("5"),
                    effective_from_cycle_id=1,
                    created_by=admin.id,
                ),
                PayrollConceptRate(
                    concept_id=dispatch.id,
                    amount=Decimal("10"),
                    effective_from_cycle_id=1,
                    created_by=admin.id,
                ),
                PayrollRecord(
                    cycle_id=1,
                    import_id=payroll_import.id,
                    employee_id=driver.id,
                    source_type="DR",
                    cost_center="DR",
                    role_type="DRIVER",
                    source_employee_name=driver.employee_name,
                    source_row_number=2,
                    source_row_hash="a" * 64,
                    source_person_slot="OPERATOR",
                    work_date=date(2026, 5, 22),
                    status=None,
                    dispatch_flag=Decimal("1"),
                    event_flag=Decimal("1"),
                ),
                PayrollRecord(
                    cycle_id=1,
                    import_id=payroll_import.id,
                    employee_id=driver.id,
                    source_type="DR",
                    cost_center="DR",
                    role_type="DRIVER",
                    source_employee_name=driver.employee_name,
                    source_row_number=3,
                    source_row_hash="b" * 64,
                    source_person_slot="OPERATOR",
                    work_date=date(2026, 5, 22),
                    status="OK",
                    dispatch_flag=Decimal("2"),
                    event_flag=Decimal("4"),
                ),
                PayrollRecord(
                    cycle_id=1,
                    import_id=payroll_import.id,
                    employee_id=driver.id,
                    source_type="DR",
                    cost_center="DR",
                    role_type="DRIVER",
                    source_employee_name=driver.employee_name,
                    source_row_number=4,
                    source_row_hash="c" * 64,
                    source_person_slot="OPERATOR",
                    work_date=date(2026, 5, 23),
                    status="OK",
                    dispatch_flag=Decimal("2"),
                ),
                PayrollRecord(
                    cycle_id=1,
                    import_id=payroll_import.id,
                    employee_id=assistant.id,
                    source_type="DR",
                    cost_center="DR",
                    role_type="ASSISTANT",
                    source_employee_name=assistant.employee_name,
                    source_row_number=5,
                    source_row_hash="d" * 64,
                    source_person_slot="AUXILIARY",
                    work_date=date(2026, 5, 22),
                    dispatch_flag=Decimal("99"),
                ),
            ]
        )
        db.commit()
        return driver.id, assistant.id


def test_settlement_builds_dynamic_calendar_concepts_units_rates_and_totals(
    client,
    db_factory,
):
    driver_id, _ = seed_settlement(db_factory)

    response = client.get(
        (
            f"/api/settlements?cycle_id=1&employee_id={driver_id}"
            "&cost_center=DR&role_type=DRIVER"
        ),
        headers=auth_headers(client),
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["dates"]) == 31
    assert body["dates"][0] == {
        "date": "2026-05-22",
        "label": "22-05",
        "weekday": "vie",
        "is_holiday": False,
        "holiday_names": [],
    }
    assert body["dates"][-1]["date"] == "2026-06-21"
    assert [row["row_type"] for row in body["rows"]] == [
        "concept",
        "concept",
        "total_to_pay",
        "variable_daily",
        "worked_day",
        "week_corrida",
        "production_total",
    ]
    event, dispatch, total_to_pay, variable_daily, worked_day, week_corrida, production_total = body["rows"]
    assert Decimal(event["units"]) == Decimal("5")
    assert Decimal(event["total"]) == Decimal("25")
    assert Decimal(dispatch["units"]) == Decimal("5")
    assert Decimal(dispatch["total"]) == Decimal("50")
    assert Decimal(body["daily_totals"][0]["value"]) == Decimal("55")
    assert Decimal(body["daily_totals"][1]["value"]) == Decimal("20")
    assert Decimal(body["total_to_pay"]) == Decimal("75")
    assert Decimal(total_to_pay["total"]) == Decimal("75")
    assert Decimal(variable_daily["daily_values"][0]["value"]) == Decimal("55")
    assert Decimal(worked_day["daily_values"][0]["value"]) == Decimal("5")
    assert Decimal(worked_day["daily_values"][1]["value"]) == Decimal("1")
    assert Decimal(worked_day["daily_values"][2]["value"]) == Decimal("0")
    assert Decimal(week_corrida["total"]) == Decimal("12.5")
    assert Decimal(body["week_corrida"]) == Decimal("12.5")
    assert Decimal(production_total["total"]) == Decimal("87.5")
    assert Decimal(body["production_total"]) == Decimal("87.5")
    assert body["statuses"][0]["status"] == "OK"


def test_settlement_marks_holiday_dates_and_uses_them_for_week_corrida(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        db.add(
            PayrollHoliday(
                holiday_date=date(2026, 5, 22),
                holiday_name="Feriado de prueba",
                holiday_scope="CUSTOM",
                active=True,
                is_default=False,
            )
        )
        db.commit()

    response = client.get(
        (
            f"/api/settlements?cycle_id=1&employee_id={driver_id}"
            "&cost_center=DR&role_type=DRIVER"
        ),
        headers=auth_headers(client),
    )

    assert response.status_code == 200
    body = response.json()
    first_date = body["dates"][0]
    assert first_date["is_holiday"] is True
    assert first_date["holiday_names"] == ["Feriado de prueba"]
    assert Decimal(body["week_corrida"]) == Decimal("25")


def test_cycle_start_worked_day_adds_missing_weekdays_even_when_first_day_has_zero_variable(client, db_factory):
    with db_factory() as db:
        admin = db.scalar(select(User).where(User.username == "admin"))
        db.add(
            PayrollCycle(
                id=2,
                cycle_name="Ciclo Sabado 2026",
                start_date=date(2026, 5, 23),
                end_date=date(2026, 5, 24),
            )
        )
        worker = Employee(employee_name="Inicio Sabado", role_type="DRIVER")
        db.add(worker)
        db.flush()
        payroll_import = PayrollImport(
            cycle_id=2,
            source_type="DR",
            cost_center="DR",
            file_name="sabado.xlsx",
            imported_by=admin.id,
            rows_imported=2,
        )
        db.add(payroll_import)
        db.flush()
        concept = PayrollConcept(
            concept_code="EVENT_SAT",
            concept_name="Evento Sabado",
            db_field="event_flag",
            source_type="DR",
            cost_center="DR",
            role_type="DRIVER",
            display_order=1,
        )
        db.add(concept)
        db.flush()
        db.add(
            PayrollConceptRate(
                concept_id=concept.id,
                amount=Decimal("5"),
                effective_from_cycle_id=2,
                created_by=admin.id,
            )
        )
        db.add_all(
            [
                PayrollRecord(
                    cycle_id=2,
                    import_id=payroll_import.id,
                    employee_id=worker.id,
                    source_type="DR",
                    cost_center="DR",
                    role_type="DRIVER",
                    source_employee_name=worker.employee_name,
                    source_row_number=10,
                    source_row_hash="x" * 64,
                    source_person_slot="OPERATOR",
                    work_date=date(2026, 5, 23),
                    event_flag=Decimal("0"),
                ),
                PayrollRecord(
                    cycle_id=2,
                    import_id=payroll_import.id,
                    employee_id=worker.id,
                    source_type="DR",
                    cost_center="DR",
                    role_type="DRIVER",
                    source_employee_name=worker.employee_name,
                    source_row_number=11,
                    source_row_hash="y" * 64,
                    source_person_slot="OPERATOR",
                    work_date=date(2026, 5, 24),
                    event_flag=Decimal("1"),
                ),
            ]
        )
        db.commit()
        worker_id = worker.id

    response = client.get(
        f"/api/settlements?cycle_id=2&employee_id={worker_id}&cost_center=DR&role_type=DRIVER",
        headers=auth_headers(client),
    )

    assert response.status_code == 200
    worked_day_row = next(row for row in response.json()["rows"] if row["row_type"] == "worked_day")
    assert Decimal(worked_day_row["daily_values"][0]["value"]) == Decimal("5")
    assert Decimal(worked_day_row["daily_values"][1]["value"]) == Decimal("1")


@pytest.mark.parametrize(
    ("status", "variable_amount", "expected"),
    [
        ("OK", Decimal("0"), Decimal("0")),
        ("OK", Decimal("3"), Decimal("1")),
        ("Licencia", Decimal("5"), Decimal("0")),
        ("Vacaciones", Decimal("5"), Decimal("0")),
        ("Libre compensatorio", Decimal("5"), Decimal("0")),
        ("Descanso", Decimal("5"), Decimal("0")),
        ("Feriado", Decimal("0"), Decimal("0")),
        ("Feriado", Decimal("3"), Decimal("1")),
        ("Inasistencia", Decimal("0"), Decimal("1")),
        ("Sin Producción", Decimal("0"), Decimal("1")),
    ],
)
def test_worked_day_value_matches_status_rules(status, variable_amount, expected):
    assert (
        SettlementEngine._worked_day_value(
            status=status,
            variable_amount=variable_amount,
        )
        == expected
    )


def test_settlement_production_total_includes_manual_adjustments(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        db.add_all(
            [
                PayrollManualAdjustment(
                    cycle_id=1,
                    employee_id=driver_id,
                    cost_center="ALL",
                    role_type="ALL",
                    adjustment_type="VACATION",
                    adjustment_name="Vacaciones",
                    amount=Decimal("10"),
                ),
                PayrollManualAdjustment(
                    cycle_id=1,
                    employee_id=driver_id,
                    cost_center="ALL",
                    role_type="ALL",
                    adjustment_type="BONUS",
                    adjustment_name="Bono especial",
                    units=Decimal("3"),
                    amount=Decimal("7"),
                ),
                PayrollManualAdjustment(
                    cycle_id=1,
                    employee_id=driver_id,
                    cost_center="ALL",
                    role_type="ALL",
                    adjustment_type="BONUS",
                    adjustment_name="Bono asistencia",
                    units=Decimal("2"),
                    amount=Decimal("4"),
                ),
                PayrollManualAdjustment(
                    cycle_id=1,
                    employee_id=driver_id,
                    cost_center="ALL",
                    role_type="ALL",
                    adjustment_type="DISCOUNT",
                    adjustment_name="Descuento",
                    amount=Decimal("3"),
                ),
            ]
        )
        db.commit()

    response = client.get(
        (
            f"/api/settlements?cycle_id=1&employee_id={driver_id}"
            "&cost_center=DR&role_type=DRIVER"
        ),
        headers=auth_headers(client),
    )

    assert response.status_code == 200
    body = response.json()
    production_total = next(
        row for row in body["rows"] if row["row_type"] == "production_total"
    )
    vacation_row = next(
        row for row in body["rows"] if row["row_type"] == "adjustment_vacation"
    )
    bonus_rows = [row for row in body["rows"] if row["row_type"] == "adjustment_bonus"]
    discount_row = next(
        row for row in body["rows"] if row["row_type"] == "adjustment_discount"
    )
    assert Decimal(body["total_to_pay"]) == Decimal("75")
    assert Decimal(body["week_corrida"]) == Decimal("12.5")
    assert Decimal(vacation_row["total"]) == Decimal("10")
    assert len(bonus_rows) == 2
    assert [row["concept_name"] for row in bonus_rows] == ["Bono especial", "Bono asistencia"]
    assert Decimal(bonus_rows[0]["units"]) == Decimal("3")
    assert Decimal(bonus_rows[0]["rate"]) == Decimal("7")
    assert Decimal(bonus_rows[0]["total"]) == Decimal("21")
    assert Decimal(bonus_rows[1]["units"]) == Decimal("2")
    assert Decimal(bonus_rows[1]["rate"]) == Decimal("4")
    assert Decimal(bonus_rows[1]["total"]) == Decimal("8")
    assert Decimal(discount_row["total"]) == Decimal("3")
    assert Decimal(production_total["total"]) == Decimal("123.5")
    assert Decimal(body["production_total"]) == Decimal("123.5")


def test_settlement_employee_options_are_filtered_by_context(client, db_factory):
    driver_id, assistant_id = seed_settlement(db_factory)
    headers = auth_headers(client)

    drivers = client.get(
        "/api/settlements/employees?cycle_id=1&cost_center=DR&role_type=DRIVER",
        headers=headers,
    )
    assistants = client.get(
        "/api/settlements/employees?cycle_id=1&cost_center=DR&role_type=ASSISTANT",
        headers=headers,
    )

    assert drivers.status_code == 200
    assert drivers.json() == [{"id": driver_id, "employee_name": "Chofer Uno", "contract_type": None, "rut": None, "email": None, "cargo": None}]
    assert assistants.status_code == 200
    assert assistants.json() == [{"id": assistant_id, "employee_name": "Auxiliar Uno", "contract_type": None, "rut": None, "email": None, "cargo": None}]


def test_search_employee_options_use_real_workers_and_filters(client, db_factory):
    driver_id, assistant_id = seed_settlement(db_factory)
    headers = auth_headers(client)

    response = client.get(
        "/api/search/employees?cycle_from_id=1&cycle_to_id=1&cost_center=DR&role_type=DRIVER",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == [{"id": driver_id, "employee_name": "Chofer Uno", "contract_type": None, "rut": None, "email": None, "cargo": None}]

    response = client.get(
        "/api/search/employees?cycle_from_id=1&cycle_to_id=1&cost_center=DR&role_type=ASSISTANT",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == [{"id": assistant_id, "employee_name": "Auxiliar Uno", "contract_type": None, "rut": None, "email": None, "cargo": None}]


def test_search_records_applies_real_filters(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.get(
        "/api/search/records?cycle_from_id=1&cycle_to_id=1&cost_center=DR&role_type=DRIVER&employee_id="
        f"{driver_id}",
        headers=auth_headers(client),
    )

    assert response.status_code == 200
    assert response.json()["records_count"] == 3


def test_liquidation_combines_contexts_and_hides_empty_rows(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        worker = db.get(Employee, driver_id)
        worker.contract_type = "OLD"
        service_concept = PayrollConcept(
            concept_code="KIT_DELIVERY",
            concept_name="Entrega Kit",
            db_field="kit_delivery_flag",
            source_type="SERVICES",
            cost_center="SERVICES",
            role_type="DRIVER",
            display_order=1,
        )
        service_assistant_concept = PayrollConcept(
            concept_code="DRYING",
            concept_name="Secado",
            db_field="drying_flag",
            source_type="SERVICES",
            cost_center="SERVICES",
            role_type="ASSISTANT",
            display_order=2,
        )
        db.add_all([service_concept, service_assistant_concept])
        db.flush()
        admin = db.scalar(select(User).where(User.username == "admin"))
        payroll_import = PayrollImport(
            cycle_id=1,
            source_type="SERVICES",
            cost_center="SERVICES",
            file_name="services.xlsx",
            imported_by=admin.id,
            rows_imported=2,
        )
        db.add(payroll_import)
        db.flush()
        service_driver = Employee(employee_name=worker.employee_name, role_type="DRIVER", contract_type="OLD")
        service_assistant = Employee(employee_name=worker.employee_name, role_type="ASSISTANT", contract_type="OLD")
        db.add_all([service_driver, service_assistant])
        db.flush()
        db.add_all(
            [
                PayrollConceptRate(
                    concept_id=service_concept.id,
                    contract_type="OLD",
                    amount=Decimal("3"),
                    effective_from_cycle_id=1,
                    created_by=admin.id,
                ),
                PayrollConceptRate(
                    concept_id=service_assistant_concept.id,
                    contract_type="OLD",
                    amount=Decimal("2"),
                    effective_from_cycle_id=1,
                    created_by=admin.id,
                ),
                PayrollRecord(
                    cycle_id=1,
                    import_id=payroll_import.id,
                    employee_id=service_driver.id,
                    source_type="SERVICES",
                    cost_center="SERVICES",
                    role_type="DRIVER",
                    source_employee_name=worker.employee_name,
                    source_row_number=20,
                    source_row_hash="e" * 64,
                    source_person_slot="OPERATOR",
                    work_date=date(2026, 5, 22),
                    kit_delivery_flag=Decimal("5"),
                ),
                PayrollRecord(
                    cycle_id=1,
                    import_id=payroll_import.id,
                    employee_id=service_assistant.id,
                    source_type="SERVICES",
                    cost_center="SERVICES",
                    role_type="ASSISTANT",
                    source_employee_name=worker.employee_name,
                    source_row_number=21,
                    source_row_hash="f" * 64,
                    source_person_slot="AUXILIARY_1",
                    work_date=date(2026, 5, 23),
                    drying_flag=Decimal("4"),
                ),
            ]
        )
        db.commit()

    response = client.get(
        f"/api/liquidations?cycle_id=1&employee_id={driver_id}",
        headers=auth_headers(client),
    )

    assert response.status_code == 200
    rows = [row for row in response.json()["rows"] if row["row_type"] == "concept"]
    names = [row["concept_name"] for row in rows]
    assert "D&R Chofer - Evento" in names
    assert "D&R Chofer - Despacho / Retiro" in names
    assert "Servicios Chofer - Entrega Kit" in names
    assert "Servicios Auxiliar - Secado" in names
    assert all("Auxiliar Uno" not in row["concept_name"] for row in rows)


def test_admin_updates_consolidated_daily_cell_and_recalculates(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        worker = db.get(Employee, driver_id)
        worker.contract_type = "OLD"
        service_assistant_concept = PayrollConcept(
            concept_code="DRYING",
            concept_name="Secado",
            db_field="drying_flag",
            source_type="SERVICES",
            cost_center="SERVICES",
            role_type="ASSISTANT",
            display_order=2,
        )
        db.add(service_assistant_concept)
        db.flush()
        admin = db.scalar(select(User).where(User.username == "admin"))
        payroll_import = PayrollImport(
            cycle_id=1,
            source_type="SERVICES",
            cost_center="SERVICES",
            file_name="services.xlsx",
            imported_by=admin.id,
            rows_imported=1,
        )
        db.add(payroll_import)
        db.flush()
        service_assistant = Employee(
            employee_name=worker.employee_name,
            role_type="ASSISTANT",
            contract_type="OLD",
        )
        db.add(service_assistant)
        db.flush()
        db.add_all(
            [
                PayrollConceptRate(
                    concept_id=service_assistant_concept.id,
                    contract_type="OLD",
                    amount=Decimal("2"),
                    effective_from_cycle_id=1,
                    created_by=admin.id,
                ),
                PayrollRecord(
                    cycle_id=1,
                    import_id=payroll_import.id,
                    employee_id=service_assistant.id,
                    source_type="SERVICES",
                    cost_center="SERVICES",
                    role_type="ASSISTANT",
                    source_employee_name=worker.employee_name,
                    source_row_number=22,
                    source_row_hash="g" * 64,
                    source_person_slot="AUXILIARY_1",
                    work_date=date(2026, 5, 23),
                    drying_flag=Decimal("4"),
                ),
            ]
        )
        db.commit()
        concept_id = service_assistant_concept.id

    response = client.post(
        "/api/liquidations/cells",
        headers=auth_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "updates": [
                {
                    "concept_id": concept_id,
                    "work_date": "2026-05-23",
                    "value": "7",
                }
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    row = next(row for row in body["rows"] if row["concept_id"] == concept_id)
    daily_value = next(item for item in row["daily_values"] if item["date"] == "2026-05-23")
    assert Decimal(daily_value["value"]) == Decimal("7")
    assert Decimal(row["units"]) == Decimal("7")
    with db_factory() as db:
        override = db.scalar(
            select(PayrollCellOverride).where(
                PayrollCellOverride.concept_id == concept_id,
                PayrollCellOverride.work_date == date(2026, 5, 23),
            )
        )
        assert override is not None
        assert override.override_value == Decimal("7")


def test_reserved_record_field_cannot_be_used_as_concept(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        db.add(
            PayrollConcept(
                concept_code="RETRIEVAL_RESERVED",
                concept_name="Retiro reservado",
                db_field="retrieval_flag",
                source_type="DR",
                cost_center="DR",
                role_type="DRIVER",
                display_order=3,
            )
        )
        db.commit()

    response = client.get(
        (
            f"/api/settlements?cycle_id=1&employee_id={driver_id}"
            "&cost_center=DR&role_type=DRIVER"
        ),
        headers=auth_headers(client),
    )

    assert response.status_code == 400
    assert "reservado" in response.json()["detail"]


def test_admin_creates_rate_version_audits_and_recalculates(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        admin = db.scalar(select(User).where(User.username == "admin"))
        event = db.scalar(select(PayrollConcept).where(PayrollConcept.concept_code == "EVENT"))
        db.add(
            PayrollCycle(
                id=2,
                cycle_name="Ciclo Julio 2026",
                start_date=date(2026, 6, 22),
                end_date=date(2026, 7, 21),
            )
        )
        payroll_import = PayrollImport(
            cycle_id=2,
            source_type="DR",
            cost_center="DR",
            file_name="july.xlsx",
            imported_by=admin.id,
            rows_imported=1,
        )
        db.add(payroll_import)
        db.flush()
        db.add(
            PayrollRecord(
                cycle_id=2,
                import_id=payroll_import.id,
                employee_id=driver_id,
                source_type="DR",
                cost_center="DR",
                role_type="DRIVER",
                source_employee_name="Chofer Uno",
                source_row_number=2,
                source_row_hash="e" * 64,
                source_person_slot="OPERATOR",
                work_date=date(2026, 6, 22),
                event_flag=Decimal("2"),
            )
        )
        db.commit()
        event_id = event.id

    response = client.post(
        "/api/settlements/rates",
        headers=auth_headers(client),
        json={
            "cycle_id": 2,
            "employee_id": driver_id,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [{"concept_id": event_id, "amount": "7.5000", "apply_mode": "FROM_CYCLE_FORWARD"}],
        },
    )

    assert response.status_code == 200
    event_row = next(row for row in response.json()["rows"] if row["concept_id"] == event_id)
    assert Decimal(event_row["rate"]) == Decimal("7.5")
    assert Decimal(event_row["total"]) == Decimal("15")
    with db_factory() as db:
        rates = db.scalars(
            select(PayrollConceptRate)
            .where(PayrollConceptRate.concept_id == event_id)
            .order_by(PayrollConceptRate.id)
        ).all()
        assert [rate.amount for rate in rates] == [Decimal("5"), Decimal("7.5")]
        assert rates[0].effective_to_cycle_id == 1
        assert rates[1].effective_from_cycle_id == 2
        assert rates[1].created_by is not None
        actions = {
            item.action_type
            for item in db.scalars(select(PayrollAuditLog)).all()
        }
        assert "RATE_FORWARD_CREATED" in actions


def test_non_admin_cannot_edit_rates(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    token = login(client, "consulta", "consulta-password")
    response = client.post(
        "/api/settlements/rates",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [{"concept_id": 1, "amount": "7", "apply_mode": "FROM_CYCLE_FORWARD"}],
        },
    )
    assert response.status_code == 403


def test_admin_updates_single_daily_cell_and_recalculates(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.post(
        "/api/settlements/cells",
        headers=auth_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [
                {
                    "concept_id": 2,
                    "work_date": "2026-05-23",
                    "value": "5",
                }
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    dispatch = next(row for row in body["rows"] if row["concept_code"] == "DISPATCH_RETRIEVAL")
    total_row = next(row for row in body["rows"] if row["row_type"] == "total_to_pay")
    assert Decimal(dispatch["units"]) == Decimal("8")
    assert Decimal(dispatch["total"]) == Decimal("80")
    assert Decimal(total_row["total"]) == Decimal("105")
    assert Decimal(body["production_total"]) == Decimal("122.5")

    with db_factory() as db:
        updated = db.scalar(select(PayrollRecord).where(PayrollRecord.id == 3))
        assert updated.dispatch_flag == Decimal("2")
        override = db.scalar(select(PayrollCellOverride))
        assert override.override_value == Decimal("5")
        audit = db.scalars(
            select(PayrollAuditLog).where(
                PayrollAuditLog.action_type == "UPDATE_DAILY_CELL_OVERRIDE"
            )
        ).all()
        assert len(audit) == 1
        assert audit[0].field_name == "override_value"


def test_admin_updates_daily_status_and_recalculates_week_corrida(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    response = client.post(
        "/api/settlements/statuses",
        headers=auth_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [{"work_date": "2026-05-23", "status": "Licencia"}],
        },
    )
    assert response.status_code == 200
    body = response.json()
    status = next(item for item in body["statuses"] if item["date"] == "2026-05-23")
    worked_day = next(row for row in body["rows"] if row["row_type"] == "worked_day")
    target_day = next(item for item in worked_day["daily_values"] if item["date"] == "2026-05-23")
    assert status["status"] == "Licencia"
    assert Decimal(target_day["value"]) == Decimal("0")
    with db_factory() as db:
        records = db.scalars(
            select(PayrollRecord).where(PayrollRecord.work_date == date(2026, 5, 23))
        ).all()
        assert records
        assert {record.status for record in records} == {"Licencia"}
        assert db.scalar(
            select(PayrollAuditLog).where(
                PayrollAuditLog.action_type == "UPDATE_DAILY_STATUS"
            )
        ) is not None


def test_daily_status_rejects_unknown_value(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    response = client.post(
        "/api/liquidations/statuses",
        headers=auth_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "updates": [{"work_date": "2026-05-23", "status": "Otro"}],
        },
    )
    assert response.status_code == 400


def test_update_daily_cell_with_multiple_records_creates_override(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.post(
        "/api/settlements/cells",
        headers=auth_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [
                {
                    "concept_id": 2,
                    "work_date": "2026-05-22",
                    "value": "4",
                }
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    dispatch = next(row for row in body["rows"] if row["concept_code"] == "DISPATCH_RETRIEVAL")
    assert Decimal(dispatch["daily_values"][0]["value"]) == Decimal("4")
    assert Decimal(dispatch["units"]) == Decimal("6")
    with db_factory() as db:
        override = db.scalar(
            select(PayrollCellOverride).where(PayrollCellOverride.work_date == date(2026, 5, 22))
        )
        assert override.override_value == Decimal("4")


def test_admin_adds_activity_with_only_manual_override_and_recalculates(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        admin = db.scalar(select(User).where(User.username == "admin"))
        added = PayrollConcept(
            concept_code="SATURDAY_AFTER_1600",
            concept_name="Sabado > 16:00",
            db_field="saturday_after_1600_qty",
            source_type="DR",
            cost_center="DR",
            role_type="DRIVER",
            display_order=3,
        )
        db.add(added)
        db.flush()
        db.add(
            PayrollConceptRate(
                concept_id=added.id,
                amount=Decimal("20"),
                effective_from_cycle_id=1,
                created_by=admin.id,
            )
        )
        db.commit()
        added_id = added.id

    response = client.post(
        "/api/liquidations/cells",
        headers=auth_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "updates": [
                {
                    "concept_id": added_id,
                    "work_date": "2026-05-24",
                    "value": "2",
                }
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    added_row = next(row for row in body["rows"] if row["concept_id"] == added_id)
    total_row = next(row for row in body["rows"] if row["row_type"] == "total_to_pay")
    assert Decimal(added_row["units"]) == Decimal("2")
    assert Decimal(added_row["rate"]) == Decimal("20")
    assert Decimal(added_row["total"]) == Decimal("40")
    assert Decimal(total_row["total"]) == Decimal("115")

    with db_factory() as db:
        override = db.scalar(
            select(PayrollCellOverride).where(
                PayrollCellOverride.concept_id == added_id,
                PayrollCellOverride.work_date == date(2026, 5, 24),
            )
        )
        assert override is not None
        assert override.override_value == Decimal("2")


def test_admin_adds_consolidated_activity_without_context_records(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        admin = db.scalar(select(User).where(User.username == "admin"))
        added = PayrollConcept(
            concept_code="SERVICE_ASSISTANT_CLEANING",
            concept_name="Aseo",
            db_field="cleaning_flag",
            source_type="SERVICES",
            cost_center="SERVICES",
            role_type="ASSISTANT",
            display_order=1,
        )
        db.add(added)
        db.flush()
        db.add(
            PayrollConceptRate(
                concept_id=added.id,
                contract_type="OLD",
                amount=Decimal("139"),
                effective_from_cycle_id=1,
                created_by=admin.id,
            )
        )
        db.commit()
        added_id = added.id

    response = client.post(
        "/api/liquidations/cells",
        headers=auth_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "updates": [
                {
                    "concept_id": added_id,
                    "work_date": "2026-05-24",
                    "value": "1",
                }
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    added_row = next(row for row in body["rows"] if row["concept_id"] == added_id)
    assert added_row["concept_name"] == "Servicios Auxiliar - Aseo"
    assert Decimal(added_row["units"]) == Decimal("1")
    with db_factory() as db:
        override = db.scalar(
            select(PayrollCellOverride).where(
                PayrollCellOverride.concept_id == added_id,
                PayrollCellOverride.work_date == date(2026, 5, 24),
            )
        )
        assert override is not None
        assert override.cost_center == "SERVICES"
        assert override.role_type == "ASSISTANT"


def test_non_admin_cannot_edit_daily_cells(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    token = login(client, "consulta", "consulta-password")

    response = client.post(
        "/api/settlements/cells",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [
                {
                    "concept_id": 2,
                    "work_date": "2026-05-23",
                    "value": "4",
                }
            ],
        },
    )

    assert response.status_code == 403


def test_admin_creates_first_rate_and_recalculates_immediately(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        event = db.scalar(select(PayrollConcept).where(PayrollConcept.concept_code == "EVENT"))
        db.query(PayrollConceptRate).filter(
            PayrollConceptRate.concept_id == event.id
        ).delete()
        db.commit()
        event_id = event.id

    response = client.post(
        "/api/settlements/rates",
        headers=auth_headers(client),
        json={
            "cycle_id": 1,
            "employee_id": driver_id,
            "cost_center": "DR",
            "role_type": "DRIVER",
            "updates": [{"concept_id": event_id, "amount": "8.2500", "apply_mode": "FROM_CYCLE_FORWARD"}],
        },
    )

    assert response.status_code == 200
    body = response.json()
    event_row = next(row for row in body["rows"] if row["concept_id"] == event_id)
    assert Decimal(event_row["rate"]) == Decimal("8.25")
    assert Decimal(event_row["total"]) == Decimal("41.25")
    assert Decimal(body["total_to_pay"]) == Decimal("91.25")
    with db_factory() as db:
        rate = db.scalar(
            select(PayrollConceptRate).where(PayrollConceptRate.concept_id == event_id)
        )
        assert rate.amount == Decimal("8.25")
        assert rate.effective_from_cycle_id == 1
