from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal
from io import BytesIO, StringIO
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


def _excel_column_name(index: int) -> str:
    result = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def _sheet_name(settlement: dict[str, object]) -> str:
    employee = settlement["employee"]["employee_name"]
    cycle = settlement["cycle"]["cycle_name"]
    base = f"{employee} {cycle}"
    invalid = set('[]:*?/\\')
    cleaned = "".join(char for char in base if char not in invalid)
    return cleaned[:31] or "Liquidacion"


def _format_number(value: Decimal | int | float | None) -> str:
    if value is None:
        return ""
    decimal_value = Decimal(str(value))
    return str(int(decimal_value.quantize(Decimal("1"))))


def settlement_matrix(settlement: dict[str, object]) -> tuple[list[str], list[list[str]]]:
    headers = ["Actividad", "Unidades", "Tarifa", "Total"]
    headers.extend(item["label"] for item in settlement["dates"])

    employee_name = settlement["employee"]["employee_name"]
    cycle_name = settlement["cycle"]["cycle_name"]
    center_label = settlement["cost_center"] or "D&R + SERVICES"
    role_label = settlement["role_type"] or "CONSOLIDADO"

    meta_rows = [
        ["Trabajador", employee_name, "", ""],
        ["Ciclo", cycle_name, "", ""],
        ["Centro", center_label, "", ""],
        ["Vista", role_label, "", ""],
        ["", "", "", ""],
    ]
    for row in meta_rows:
        row.extend("" for _ in settlement["dates"])

    status_by_date = {item["date"]: item["status"] or "" for item in settlement["statuses"]}
    status_row = ["Estado", "", "", ""]
    status_row.extend(status_by_date.get(item["date"], "") for item in settlement["dates"])

    rows = [*meta_rows, status_row]
    for row in settlement["rows"]:
        output = [
            row["concept_name"],
            _format_number(row["units"]),
            _format_number(row["rate"]),
            _format_number(row["total"]),
        ]
        output.extend(_format_number(item["value"]) for item in row["daily_values"])
        rows.append(output)
    return headers, rows


def export_csv_bytes(settlement: dict[str, object]) -> bytes:
    headers, rows = settlement_matrix(settlement)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")


def _xlsx_cell_xml(row_index: int, column_index: int, value: str) -> str:
    cell_ref = f"{_excel_column_name(column_index)}{row_index}"
    if value == "":
        return f'<c r="{cell_ref}"/>'
    try:
        Decimal(value)
    except Exception:
        return (
            f'<c r="{cell_ref}" t="inlineStr">'
            f"<is><t>{escape(value)}</t></is></c>"
        )
    return f'<c r="{cell_ref}"><v>{escape(value)}</v></c>'


def export_xlsx_bytes(settlement: dict[str, object]) -> bytes:
    headers, rows = settlement_matrix(settlement)
    worksheet_rows = [headers, *rows]
    sheet_rows_xml: list[str] = []
    for row_index, row in enumerate(worksheet_rows, start=1):
        cells = [
            _xlsx_cell_xml(row_index, column_index, value)
            for column_index, value in enumerate(row, start=1)
        ]
        sheet_rows_xml.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    worksheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"<sheetData>{''.join(sheet_rows_xml)}</sheetData>"
        "</worksheet>"
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheets><sheet name="{escape(_sheet_name(settlement))}" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )

    workbook_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
        "</Relationships>"
    )

    root_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        "</Types>"
    )

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
        '<borders count="1"><border/></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        "</styleSheet>"
    )

    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml)
        archive.writestr("_rels/.rels", root_rels_xml)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        archive.writestr("xl/worksheets/sheet1.xml", worksheet_xml)
        archive.writestr("xl/styles.xml", styles_xml)
    return buffer.getvalue()


def export_file_name(
    *,
    settlement: dict[str, object],
    file_format: str,
    cost_center: str | None,
    role_type: str | None,
) -> str:
    employee = settlement["employee"]["employee_name"].replace(" ", "_")
    cycle_name = settlement["cycle"]["cycle_name"].replace(" ", "_")
    scope = "consolidado" if cost_center is None or role_type is None else f"{cost_center}_{role_type}"
    return f"liquidacion_{employee}_{cycle_name}_{scope}.{file_format}"
