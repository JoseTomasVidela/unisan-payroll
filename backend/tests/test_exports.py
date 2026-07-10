from __future__ import annotations

from decimal import Decimal
from io import BytesIO
from zipfile import ZipFile

from sqlalchemy import select

from app.models import PayrollExportLog, PayrollManualAdjustment
from conftest import login
from test_settlements import seed_settlement


def admin_headers(client):
    token = login(client, "admin", "admin-password")
    return {"Authorization": f"Bearer {token}"}


def user_headers(client):
    token = login(client, "consulta", "consulta-password")
    return {"Authorization": f"Bearer {token}"}


def test_export_individual_liquidation_excel(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.get(
        (
            f"/api/exports/settlement?cycle_id=1&employee_id={driver_id}"
            "&cost_center=DR&role_type=DRIVER&file_format=xlsx"
        ),
        headers=admin_headers(client),
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert "attachment;" in response.headers["content-disposition"]
    assert 'filename="Chofer Uno-Junio 2026.xlsx"' in response.headers["content-disposition"]

    archive = ZipFile(BytesIO(response.content))
    worksheet_xml = archive.read("xl/worksheets/sheet1.xml").decode("utf-8")
    assert "Trabajador" in worksheet_xml
    assert "Chofer Uno" in worksheet_xml
    assert "Actividad" in worksheet_xml
    assert "Tarifa" in worksheet_xml
    assert "Evento" in worksheet_xml
    assert "TOTAL A PAGAR" in worksheet_xml
    assert "PRODUCCION TOTAL" in worksheet_xml


def test_export_individual_liquidation_csv(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.get(
        (
            f"/api/exports/settlement?cycle_id=1&employee_id={driver_id}"
            "&cost_center=DR&role_type=DRIVER&file_format=csv"
        ),
        headers=admin_headers(client),
    )

    assert response.status_code == 200
    body = response.content.decode("utf-8-sig")
    assert "Trabajador,Chofer Uno,,," in body
    assert "Actividad,Unidades,Tarifa,Total" in body
    assert "Evento,5,5,25" in body
    assert "TOTAL A PAGAR,,," in body
    assert "PRODUCCION TOTAL,,," in body


def test_export_individual_liquidation_pdf(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)
    with db_factory() as db:
        db.add(
            PayrollManualAdjustment(
                cycle_id=1,
                employee_id=driver_id,
                cost_center="ALL",
                role_type="ALL",
                adjustment_type="BONUS",
                adjustment_name="Bono exportado",
                units=Decimal("3"),
                amount=Decimal("2000"),
            )
        )
        db.commit()

    response = client.get(
        (
            f"/api/exports/settlement?cycle_id=1&employee_id={driver_id}"
            "&cost_center=DR&role_type=DRIVER&file_format=pdf"
        ),
        headers=admin_headers(client),
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert response.content.startswith(b"%PDF-")
    assert 'filename="Chofer Uno-Junio 2026.pdf"' in response.headers["content-disposition"]
    assert b"MOVILES DE CHILE S.A." in response.content
    assert b"ANEXO DE LIQUIDACION DE SUELDO MES DE JUNIO 2026" in response.content
    assert b"Articulo 54 bis inciso tercero del Codigo del Trabajo" in response.content
    assert b"Chofer Uno" in response.content
    assert b"DESCRIPCION" in response.content
    assert b"A PAGAR" in response.content
    assert b"SEMANA CORRIDA" in response.content
    assert b"BONO EXPORTADO" in response.content
    assert b"6.000" in response.content
    assert b"TOTAL" in response.content
    assert b"FIRMA TRABAJADOR" in response.content


def test_export_from_search_uses_consolidated_scope_and_logs(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.get(
        f"/api/exports/settlement?cycle_id=1&employee_id={driver_id}&file_format=csv",
        headers=admin_headers(client),
    )

    assert response.status_code == 200

    with db_factory() as db:
        logs = db.scalars(select(PayrollExportLog).order_by(PayrollExportLog.id)).all()
        assert len(logs) == 1
        assert logs[0].export_scope == "SEARCH"
        assert logs[0].file_format == "CSV"
        assert logs[0].cycle_id == 1
        assert logs[0].employee_id == driver_id
        assert logs[0].cost_center is None
        assert logs[0].role_type is None


def test_export_logs_context_export(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.get(
        (
            f"/api/exports/settlement?cycle_id=1&employee_id={driver_id}"
            "&cost_center=DR&role_type=DRIVER&file_format=csv"
        ),
        headers=admin_headers(client),
    )

    assert response.status_code == 200

    with db_factory() as db:
        log = db.scalar(select(PayrollExportLog).where(PayrollExportLog.employee_id == driver_id))
        assert log is not None
        assert log.export_scope == "SETTLEMENT"
        assert log.file_format == "CSV"
        assert log.cost_center == "DR"
        assert log.role_type == "DRIVER"
        assert log.user_id == 1
        assert log.file_name.endswith(".csv")


def test_authenticated_user_can_export(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.get(
        f"/api/exports/settlement?cycle_id=1&employee_id={driver_id}&file_format=csv",
        headers=user_headers(client),
    )

    assert response.status_code == 200
    assert "Actividad,Unidades,Tarifa,Total" in response.content.decode("utf-8-sig")


def test_export_requires_authentication(client, db_factory):
    driver_id, _ = seed_settlement(db_factory)

    response = client.get(
        f"/api/exports/settlement?cycle_id=1&employee_id={driver_id}&file_format=csv"
    )

    assert response.status_code == 401
