from __future__ import annotations

from datetime import date, time
from io import BytesIO

from openpyxl import Workbook
from sqlalchemy import func, select

from app.importer import DR_HEADERS, SERVICES_HEADERS, cycle_definition_for_date
from app.models import PayrollCycle, PayrollRecord
from conftest import login


def workbook_bytes(headers, rows) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Base Datos"
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


def auth_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def test_import_dr_creates_driver_and_valid_assistant(client, db_factory):
    row = [
        "Operador Uno", "Auxiliar Uno", "OP-1", date(2026, 5, 22), None,
        time(2, 30), "OK", 1, 2, 3, 0, 0, 1, 1.5, 0, 0, 4, 0, 0, None,
        1, 1, 0, 2, 3, 1, 5, 6,
    ]
    content = workbook_bytes(DR_HEADERS, [row])

    response = client.post(
        "/api/imports/DR",
        headers=auth_headers(client),
        data={"confirm_reimport": "false"},
        files={"file": ("Base Producciones D&R.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 200
    assert response.json()["records_inserted"] == 2
    assert response.json()["workers_created"] == 2
    with db_factory() as db:
        records = db.scalars(select(PayrollRecord).order_by(PayrollRecord.role_type)).all()
        assert {record.source_person_slot for record in records} == {
            "OPERATOR",
            "AUXILIARY",
        }
        assert len({record.source_row_hash for record in records}) == 1
        assistant = next(record for record in records if record.role_type == "ASSISTANT")
        assert assistant.saturday_week_2_qty == 5
        assert assistant.sunday_week_2_qty == 6
        assert assistant.duration_minutes == 150


def test_possible_reimport_requires_explicit_confirmation(client, db_factory):
    row = [
        "Operador Uno", None, "OP-1", date(2026, 5, 22), None, None, "OK",
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    content = workbook_bytes(DR_HEADERS, [row])
    headers = auth_headers(client)
    request = {
        "headers": headers,
        "data": {"confirm_reimport": "false"},
        "files": {"file": ("dr.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    }
    assert client.post("/api/imports/DR", **request).status_code == 200

    warning = client.post("/api/imports/DR", **request)

    assert warning.status_code == 409
    assert warning.json()["detail"]["possible_reimports"] == 1
    with db_factory() as db:
        assert db.scalar(select(func.count(PayrollRecord.id))) == 1

    confirmed = client.post(
        "/api/imports/DR",
        headers=headers,
        data={"confirm_reimport": "true"},
        files=request["files"],
    )
    assert confirmed.status_code == 200
    assert confirmed.json()["possible_reimports_confirmed"] == 1
    with db_factory() as db:
        assert db.scalar(select(func.count(PayrollRecord.id))) == 2


def test_import_services_creates_three_person_slots(client, db_factory):
    row = [
        "Operador S", "S-1", "Auxiliar S1", "Auxiliar S2", date(2026, 6, 1),
        None, time(1, 0), "OK", 1, 2, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
        0, 0, 3.25, None, None,
    ]
    content = workbook_bytes(SERVICES_HEADERS, [row])

    response = client.post(
        "/api/imports/SERVICES",
        headers=auth_headers(client),
        data={},
        files={"file": ("servicios.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 200
    assert response.json()["records_inserted"] == 3
    with db_factory() as db:
        records = db.scalars(select(PayrollRecord)).all()
        assert {record.source_person_slot for record in records} == {
            "OPERATOR", "AUXILIARY_1", "AUXILIARY_2"
        }
        assert all(record.riles_suction_flag == 3.25 for record in records)


def test_missing_cycle_is_created_automatically(client, db_factory):
    row = [
        "Operador Uno", None, "OP-1", date(2026, 7, 1), None, None, "OK",
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    content = workbook_bytes(DR_HEADERS, [row])

    response = client.post(
        "/api/imports/DR",
        headers=auth_headers(client),
        data={},
        files={"file": ("dr.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 200
    assert response.json()["cycles_created"] == 1
    with db_factory() as db:
        cycle = db.scalar(
            select(PayrollCycle).where(PayrollCycle.cycle_name == "Ciclo Julio 2026")
        )
        record = db.scalar(select(PayrollRecord))
        assert cycle.start_date == date(2026, 6, 22)
        assert cycle.end_date == date(2026, 7, 21)
        assert record.cycle_id == cycle.id


def test_user_without_import_permission_is_rejected(client):
    token = login(client, "consulta", "consulta-password")
    content = workbook_bytes(DR_HEADERS, [])

    response = client.post(
        "/api/imports/DR",
        headers={"Authorization": f"Bearer {token}"},
        data={},
        files={"file": ("dr.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 403


def test_invalid_xlsx_is_rejected(client):
    response = client.post(
        "/api/imports/DR",
        headers=auth_headers(client),
        data={},
        files={"file": ("dr.xlsx", b"not-an-excel", "application/octet-stream")},
    )

    assert response.status_code == 400
    assert "xlsx válido" in response.json()["detail"]


def test_import_detects_cycle_automatically(client):
    row = [
        "Operador Uno", None, "OP-1", date(2026, 6, 1), None, None, "OK",
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    content = workbook_bytes(DR_HEADERS, [row])

    response = client.post(
        "/api/imports/DR",
        headers=auth_headers(client),
        data={},
        files={"file": ("dr.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 200
    assert response.json()["cycle_ids"] == [1]


def test_import_accepts_multiple_cycles(client, db_factory):
    first = [
        "Operador Uno", None, "OP-1", date(2026, 6, 1), None, None, "OK",
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    second = first.copy()
    second[3] = date(2026, 7, 1)
    content = workbook_bytes(DR_HEADERS, [first, second])

    response = client.post(
        "/api/imports/DR",
        headers=auth_headers(client),
        data={},
        files={"file": ("dr.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 200
    assert len(response.json()["cycle_ids"]) == 2
    assert len(response.json()["import_ids"]) == 2
    assert response.json()["cycles_created"] == 1
    with db_factory() as db:
        records = db.scalars(select(PayrollRecord).order_by(PayrollRecord.work_date)).all()
        assert records[0].cycle_id != records[1].cycle_id


def test_cycle_definition_uses_closing_month():
    april_22 = cycle_definition_for_date(date(2025, 4, 22))
    may_21 = cycle_definition_for_date(date(2026, 5, 21))

    assert april_22.cycle_name == "Ciclo Mayo 2025"
    assert april_22.start_date == date(2025, 4, 22)
    assert april_22.end_date == date(2025, 5, 21)
    assert may_21.cycle_name == "Ciclo Mayo 2026"
    assert may_21.start_date == date(2026, 4, 22)
    assert may_21.end_date == date(2026, 5, 21)


def test_invalid_date_rejects_entire_import(client, db_factory):
    valid = [
        "Operador Uno", None, "OP-1", date(2026, 6, 1), None, None, "OK",
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    invalid = valid.copy()
    invalid[3] = "fecha mala"
    content = workbook_bytes(DR_HEADERS, [valid, invalid])

    response = client.post(
        "/api/imports/DR",
        headers=auth_headers(client),
        data={},
        files={"file": ("dr.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 400
    assert "Fecha Inicial inválida" in response.json()["detail"]
    with db_factory() as db:
        assert db.scalar(select(func.count(PayrollRecord.id))) == 0


def test_cycles_endpoint_lists_historical_cycles_after_import(client):
    row = [
        "Operador Uno", None, "OP-1", date(2025, 4, 22), None, None, "OK",
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    content = workbook_bytes(DR_HEADERS, [row])
    headers = auth_headers(client)
    assert client.post(
        "/api/imports/DR",
        headers=headers,
        data={},
        files={"file": ("historico.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    ).status_code == 200

    cycles = client.get("/api/cycles", headers=headers)

    assert cycles.status_code == 200
    assert "Ciclo Mayo 2025" in {cycle["cycle_name"] for cycle in cycles.json()}


def test_search_filters_using_payroll_record_cycle_ids(client, db_factory):
    with db_factory() as db:
        db.add(
            PayrollCycle(
                id=2,
                cycle_name="Ciclo Julio 2026",
                start_date=date(2026, 6, 22),
                end_date=date(2026, 7, 21),
            )
        )
        db.commit()
    first = [
        "Operador Uno", None, "OP-1", date(2026, 6, 1), None, None, "OK",
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    second = first.copy()
    second[3] = date(2026, 7, 1)
    content = workbook_bytes(DR_HEADERS, [first, second])
    headers = auth_headers(client)
    assert client.post(
        "/api/imports/DR",
        headers=headers,
        data={},
        files={"file": ("historico.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    ).status_code == 200

    result = client.get(
        "/api/search/records?cycle_from_id=1&cycle_to_id=1",
        headers=headers,
    )

    assert result.status_code == 200
    assert result.json()["cycle_ids"] == [1]
    assert result.json()["records_count"] == 1
