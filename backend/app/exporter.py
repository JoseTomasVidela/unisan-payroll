from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal
from io import BytesIO, StringIO
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


BRAND_BLUE = (0.180, 0.525, 0.667)
PDF_WEEKDAY_LABELS = {
    "lun": "Lun",
    "mar": "Mar",
    "mie": "Mie",
    "jue": "Jue",
    "vie": "Vie",
    "sab": "Sab",
    "dom": "Dom",
}
STATUS_LABELS = {
    "libre compensatorio": "Libre Comp.",
    "sin produccion": "Sin Prod.",
    "sin producción": "Sin Prod.",
    "inasistencia": "Inasis.",
    "vacaciones": "Vac.",
    "descanso": "Desc.",
    "feriado": "Feriado",
    "licencia": "Licencia",
}
LOGO_PATH = Path(__file__).resolve().parents[2] / "grafic" / "UNISANLOGO.jpg"
COMPANY_HEADER_LINES = [
    "MOVILES DE CHILE S.A.",
    "RUT: 96.702.560-7",
    "LAS ESTERAS NORTE 2351, QUILICURA",
]
LEGAL_SUBTITLE = "Articulo 54 bis inciso tercero del Codigo del Trabajo"
RECEIPT_LINES = [
    "CERTIFICO QUE HE RECIBIDO DE MOVILES DE CHILE S.A. MI ENTERA",
    "SATISFACCION EL MONTO INDICADO POR CONCEPTO DE BONO",
    "Y NO TENGO CARGO NI COBRO ALGUNO POSTERIOR QUE HACER",
]


def export_audit_pdf_bytes(audit_date: date, entries: list[object]) -> bytes:
    page_width, page_height = 842, 595
    margin = 36
    column_widths = (185, 145, 440)

    def pdf_text(value: object) -> str:
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace("(", "\\(")
            .replace(")", "\\)")
        )

    def wrap(value: str, max_chars: int) -> list[str]:
        words = str(value).split()
        if not words:
            return [""]
        lines, current = [], words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if len(candidate) <= max_chars:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    pages: list[str] = []
    stream: list[str] = []
    y = page_height - margin

    def text_line(x: float, baseline: float, value: str, size: int = 9, bold: bool = False) -> None:
        font = "F2" if bold else "F1"
        stream.append(f"BT /{font} {size} Tf 1 0 0 1 {x:.1f} {baseline:.1f} Tm ({pdf_text(value)}) Tj ET")

    def line(x1: float, y1: float, x2: float, y2: float) -> None:
        stream.append(f"{x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S")

    def start_page() -> None:
        nonlocal stream, y
        stream = ["0.25 0.25 0.25 RG", "0.8 w"]
        y = page_height - margin
        text_line(margin, y, "UNISAN - Auditoría", 16, True)
        text_line(margin, y - 20, f"Acciones realizadas el {audit_date.strftime('%d-%m-%Y')}", 10)
        y -= 44
        stream.append("0.180 0.525 0.667 rg")
        stream.append(f"{margin} {y - 24} {sum(column_widths)} 24 re f")
        stream.append("0 0 0 rg")
        headings = ("Fecha y hora", "Usuario", "Acción realizada")
        x = margin
        for heading, width in zip(headings, column_widths):
            text_line(x + 6, y - 16, heading, 9, True)
            x += width
        y -= 24

    def finish_page() -> None:
        pages.append("\n".join(stream))

    start_page()
    for entry in entries:
        action_lines = wrap(getattr(entry, "action"), 76)
        row_height = max(26, 10 + len(action_lines) * 12)
        if y - row_height < margin + 16:
            finish_page()
            start_page()
        action_date = getattr(entry, "action_date")
        values = (
            action_date.strftime("%d-%m-%Y %H:%M:%S"),
            getattr(entry, "username"),
        )
        x = margin
        text_line(x + 6, y - 17, values[0], 9)
        x += column_widths[0]
        text_line(x + 6, y - 17, values[1], 9)
        x += column_widths[1]
        for index, action_line in enumerate(action_lines):
            text_line(x + 6, y - 17 - index * 12, action_line, 9)
        line(margin, y - row_height, margin + sum(column_widths), y - row_height)
        y -= row_height
    if not entries:
        text_line(margin + 6, y - 18, "No hay acciones registradas para esta fecha.", 9)
    finish_page()

    objects: list[bytes] = []
    page_object_numbers: list[int] = []
    content_object_numbers: list[int] = []
    next_object = 5
    for _ in pages:
        page_object_numbers.append(next_object)
        content_object_numbers.append(next_object + 1)
        next_object += 2
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{number} 0 R" for number in page_object_numbers)
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    for page_number, content_number, content in zip(page_object_numbers, content_object_numbers, pages):
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width} {page_height}] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_number} 0 R >>".encode("ascii")
        )
        encoded = content.encode("cp1252", "replace")
        objects.append(f"<< /Length {len(encoded)} >>\nstream\n".encode("ascii") + encoded + b"\nendstream")

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode("ascii")
    )
    return bytes(output)


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


def _format_peso_number(value: Decimal | int | float | None) -> str:
    if value is None or value == "":
        return ""
    decimal_value = Decimal(str(value))
    integer_value = int(decimal_value.quantize(Decimal("1")))
    return f"{integer_value:,}".replace(",", ".")


def _format_status_label(value: str | None) -> str:
    if not value:
        return ""
    status_parts = [part.strip() for part in str(value).split("/") if part.strip()]
    if not status_parts:
        return ""
    formatted_parts = []
    for part in status_parts:
        normalized = part.casefold()
        formatted_parts.append(STATUS_LABELS.get(normalized, part))
    return " / ".join(formatted_parts)


def _cycle_title_month(cycle_name: str | None) -> str:
    if not cycle_name:
        return ""
    normalized = " ".join(str(cycle_name).strip().split())
    if normalized.casefold().startswith("ciclo "):
        normalized = normalized[6:].strip()
    return normalized.upper()


def _cycle_file_month(cycle_name: str | None) -> str:
    if not cycle_name:
        return "Ciclo"
    normalized = " ".join(str(cycle_name).strip().split())
    if normalized.casefold().startswith("ciclo "):
        normalized = normalized[6:].strip()
    return normalized or "Ciclo"


def _file_component(value: str) -> str:
    invalid = set('<>:"/\\|?*')
    cleaned = "".join(character for character in str(value) if character not in invalid)
    return " ".join(cleaned.strip().split()) or "exportacion"


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

    status_by_date = {item["date"]: _format_status_label(item["status"]) for item in settlement["statuses"]}
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


def export_softland_xlsx_bytes(rows: list[list[object]]) -> bytes:
    worksheet_rows = [["FICHA", "CODI", "MES AÑO", "VALOR"], *rows]
    sheet_rows_xml: list[str] = []
    for row_index, row in enumerate(worksheet_rows, start=1):
        cells = [
            _xlsx_cell_xml(row_index, column_index, str(value))
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
        '<sheets><sheet name="Softland" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )
    workbook_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    root_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml)
        archive.writestr("_rels/.rels", root_rels_xml)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        archive.writestr("xl/worksheets/sheet1.xml", worksheet_xml)
    return buffer.getvalue()


def export_pdf_bytes(settlement: dict[str, object]) -> bytes:
    page_width = 595
    page_height = 842
    margin = 34
    table_row_height = 18
    table_col_widths = [239, 50, 78, 78, 82]
    table_headers = ["DESCRIPCION", "CANT", "P. UNITARIO", "MONTO", "A PAGAR"]
    week_table_headers = table_headers

    employee_name = settlement["employee"]["employee_name"]
    cycle_name = settlement["cycle"]["cycle_name"]
    employee_rut = settlement["employee"].get("rut") or ""
    title = f"ANEXO DE LIQUIDACION DE SUELDO MES DE {_cycle_title_month(cycle_name)}"
    logo_bytes = LOGO_PATH.read_bytes() if LOGO_PATH.exists() else None

    def _jpeg_dimensions(raw_bytes: bytes) -> tuple[int, int]:
        if raw_bytes[:2] != b"\xff\xd8":
            raise ValueError("Logo JPG invalido.")
        index = 2
        while index < len(raw_bytes):
            while index < len(raw_bytes) and raw_bytes[index] == 0xFF:
                index += 1
            if index >= len(raw_bytes):
                break
            marker = raw_bytes[index]
            index += 1
            if marker in {0xD8, 0xD9}:
                continue
            if index + 1 >= len(raw_bytes):
                break
            segment_length = int.from_bytes(raw_bytes[index:index + 2], "big")
            if segment_length < 2 or index + segment_length > len(raw_bytes):
                break
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                height = int.from_bytes(raw_bytes[index + 3:index + 5], "big")
                width = int.from_bytes(raw_bytes[index + 5:index + 7], "big")
                return width, height
            index += segment_length
        raise ValueError("No fue posible leer dimensiones del logo JPG.")

    def _pdf_escape_text(value: str) -> str:
        escaped = str(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        return escaped

    def _latin_text(value: str) -> str:
        normalized = str(value).replace("—", "-").replace("–", "-").replace("…", "...")
        return _pdf_escape_text(normalized.encode("cp1252", "replace").decode("cp1252"))

    def _wrap_text(value: str, max_chars: int) -> list[str]:
        words = str(value).split()
        if not words:
            return [""]
        lines: list[str] = []
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if len(candidate) <= max_chars:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def _line(stream: list[str], x1: int, y1: int, x2: int, y2: int) -> None:
        stream.append(f"{x1} {y1} m {x2} {y2} l S")

    def _rect(stream: list[str], x: int, y: int, width: int, height: int, fill_rgb: tuple[float, float, float] | None = None) -> None:
        if fill_rgb is not None:
            r, g, b = fill_rgb
            stream.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
            stream.append(f"{x} {y} {width} {height} re B")
            stream.append("0 0 0 rg")
        else:
            stream.append(f"{x} {y} {width} {height} re S")

    def _text(
        stream: list[str],
        x: int,
        y: int,
        text: str,
        *,
        size: int = 9,
        font: str = "F1",
        color: tuple[float, float, float] | None = None,
    ) -> None:
        if color is not None:
            stream.append(f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg")
        stream.append(f"BT /{font} {size} Tf 1 0 0 1 {x} {y} Tm ({_latin_text(text)}) Tj ET")
        if color is not None:
            stream.append("0 0 0 rg")

    def _draw_logo(stream: list[str], x: int, y: int, width: int, height: int) -> None:
        if logo_bytes:
            stream.append("q")
            stream.append(f"{width} 0 0 {height} {x} {y} cm")
            stream.append("/Im1 Do")
            stream.append("Q")
        else:
            _rect(stream, x, y, width, height, (0.945, 0.961, 0.973))
            _text(stream, x + 14, y + 15, "[LOGO UNISAN]", size=10, font="F2")

    def _draw_header(stream: list[str], page_number: int, total_pages: int) -> int:
        top = page_height - margin
        logo_width = 102
        logo_height = 36
        _draw_logo(stream, margin, top - logo_height, logo_width, logo_height)
        header_x = margin + 118
        current_y = top - 8
        for line in COMPANY_HEADER_LINES:
            _text(stream, header_x, current_y, line, size=10, font="F2", color=BRAND_BLUE)
            current_y -= 12
        _text(
            stream,
            page_width - margin - 76,
            top - 8,
            f"Pagina {page_number}/{total_pages}",
            size=9,
            color=BRAND_BLUE,
        )
        title_top = top - 58
        title_height = 22
        subtitle_height = 18
        _rect(stream, margin, title_top - title_height, page_width - (margin * 2), title_height, (1.0, 0.973, 0.710))
        _text(stream, margin + 62, title_top - 15, title, size=13, font="F2")
        subtitle_top = title_top - title_height
        _rect(stream, margin, subtitle_top - subtitle_height, page_width - (margin * 2), subtitle_height, (1.0, 0.973, 0.710))
        _text(stream, margin + 95, subtitle_top - 12, LEGAL_SUBTITLE, size=10, font="F2")
        worker_top = subtitle_top - subtitle_height
        worker_box_width = 260
        worker_box_height = 34
        _rect(stream, margin, worker_top - worker_box_height, worker_box_width, worker_box_height, (1.0, 0.973, 0.710))
        _text(stream, margin + 12, worker_top - 13, employee_name, size=11, font="F2")
        if employee_rut:
            _text(stream, margin + 12, worker_top - 27, f"RUT: {employee_rut}", size=11, font="F2")
        return worker_top - worker_box_height - 18

    concept_rows = [row for row in settlement["rows"] if row["row_type"] == "concept"]
    week_corrida_row = next((row for row in settlement["rows"] if row["row_type"] == "week_corrida"), None)
    adjustment_rows = [
        row for row in settlement["rows"]
        if str(row["row_type"]).startswith("adjustment_") and Decimal(str(row["total"] or 0)) != 0
    ]

    def _build_main_rows() -> list[list[str]]:
        rows: list[list[str]] = []
        activity_total = Decimal(str(settlement["total_to_pay"] or 0))
        for index, row in enumerate(concept_rows):
            amount = Decimal(str(row["total"] or 0))
            rows.append([
                str(row["concept_name"]).upper(),
                _format_peso_number(row["units"]),
                _format_peso_number(row["rate"]),
                _format_peso_number(amount),
                _format_peso_number(activity_total) if index == 0 else "",
            ])
        return rows

    def _build_week_corrida_rows() -> list[list[str]]:
        if week_corrida_row is None or Decimal(str(week_corrida_row["total"] or 0)) == 0:
            return []
        amount = Decimal(str(week_corrida_row["total"] or 0))
        return [[
            "SEMANA CORRIDA",
            _format_peso_number(week_corrida_row["units"]),
            _format_peso_number(week_corrida_row["rate"]),
            _format_peso_number(amount),
            _format_peso_number(amount),
        ]]

    def _build_adjustment_rows() -> list[list[str]]:
        rows: list[list[str]] = []
        for row in adjustment_rows:
            amount = Decimal(str(row["total"] or 0))
            rows.append([
                str(row["concept_name"]).upper(),
                _format_peso_number(row["units"]),
                _format_peso_number(row["rate"]),
                _format_peso_number(amount),
                _format_peso_number(amount),
            ])
        return rows

    def _draw_table(stream: list[str], rows: list[list[str]], y_top: int, headers: list[str]) -> int:
        table_width = sum(table_col_widths)
        header_bottom = y_top - table_row_height
        _rect(stream, margin, header_bottom, table_width, table_row_height, BRAND_BLUE)
        cursor = margin
        for width in table_col_widths:
            _line(stream, cursor, y_top, cursor, header_bottom)
            cursor += width
        _line(stream, cursor, y_top, cursor, header_bottom)
        for idx, header in enumerate(headers):
            cell_x = margin + sum(table_col_widths[:idx]) + 4
            _text(stream, cell_x, header_bottom + 5, header, size=8, font="F2", color=(1, 1, 1))
        _line(stream, margin, y_top, margin + table_width, y_top)
        _line(stream, margin, header_bottom, margin + table_width, header_bottom)

        current_top = header_bottom
        for row_index, row in enumerate(rows):
            row_bottom = current_top - table_row_height
            is_total_row = row_index == len(rows) - 1 and str(row[0]).strip().upper() == "TOTAL"
            if is_total_row:
                _rect(stream, margin, row_bottom, table_width, table_row_height, (1.0, 0.973, 0.710))
            elif row_index % 2 == 0:
                _rect(stream, margin, row_bottom, table_width, table_row_height, (0.993, 0.993, 0.993))
            cursor = margin
            for width in table_col_widths:
                _line(stream, cursor, current_top, cursor, row_bottom)
                cursor += width
            _line(stream, cursor, current_top, cursor, row_bottom)
            _line(stream, margin, row_bottom, margin + table_width, row_bottom)
            for idx, cell in enumerate(row):
                cell_x = margin + sum(table_col_widths[:idx]) + 4
                text = str(cell)
                if idx == 0 and len(text) > 40:
                    text = f"{text[:39]}..."
                _text(
                    stream,
                    cell_x,
                    row_bottom + 6,
                    text,
                    size=9,
                    font="F2" if idx == 0 or is_total_row else "F1",
                )
            current_top = row_bottom
        return current_top - 10

    def _estimate_section_height(row_count: int, title_gap: int = 12) -> int:
        if row_count <= 0:
            return 0
        return title_gap + table_row_height + (row_count * table_row_height) + 10

    main_rows = _build_main_rows()
    week_rows = _build_week_corrida_rows()
    pdf_adjustment_rows = _build_adjustment_rows()

    pages: list[str] = []
    page_index = 1
    page_total_hint = 1
    stream: list[str] = ["1 w", "0 0 0 RG", "0 0 0 rg"]
    y = _draw_header(stream, page_index, 1)

    def ensure_space(required_height: int) -> None:
        nonlocal page_index, stream, y
        if y - required_height >= margin + 90:
            return
        pages.append("\n".join(stream))
        page_index += 1
        stream = ["1 w", "0 0 0 RG", "0 0 0 rg"]
        y = _draw_header(stream, page_index, page_total_hint)

    ensure_space(_estimate_section_height(len(main_rows)))
    y = _draw_table(stream, main_rows, y, table_headers)

    if week_rows:
        y -= 8
        ensure_space(_estimate_section_height(len(week_rows)))
        y = _draw_table(stream, week_rows, y, week_table_headers)

    if pdf_adjustment_rows:
        y -= 8
        ensure_space(_estimate_section_height(len(pdf_adjustment_rows)))
        y = _draw_table(stream, pdf_adjustment_rows, y, week_table_headers)

    y -= 8
    total_box_height = 18
    total_table_width = sum(table_col_widths)
    left_total_width = sum(table_col_widths[:4])
    right_total_width = table_col_widths[4]
    final_total = Decimal(str(settlement["production_total"]))

    ensure_space(110)
    _rect(stream, margin, y - total_box_height, left_total_width, total_box_height, (1.0, 0.973, 0.710))
    _rect(stream, margin + left_total_width, y - total_box_height, right_total_width, total_box_height, (1.0, 0.973, 0.710))
    _text(stream, margin + 8, y - 12, "TOTAL", size=10, font="F2")
    _text(stream, margin + left_total_width + 8, y - 12, _format_peso_number(final_total), size=10, font="F2")
    y -= total_box_height + 10
    y -= 10

    for line in RECEIPT_LINES:
        _text(stream, margin + 2, y, line, size=10, font="F1")
        y -= 14

    y -= 32
    signature_y = max(y, margin + 28)
    left_signature_width = 160
    right_signature_width = 140
    _line(stream, margin, signature_y, margin + left_signature_width, signature_y)
    _line(stream, page_width - margin - right_signature_width, signature_y, page_width - margin, signature_y)
    _text(stream, margin + 6, signature_y - 16, "FIRMA EMPLEADOR", size=10, font="F1")
    _text(stream, page_width - margin - right_signature_width + 6, signature_y - 16, "FIRMA TRABAJADOR", size=10, font="F1")

    pages.append("\n".join(stream))
    total_pages = len(pages)
    if total_pages > 1:
        pages = []
        page_index = 1
        page_total_hint = total_pages
        stream = ["1 w", "0 0 0 RG", "0 0 0 rg"]
        y = _draw_header(stream, page_index, total_pages)
        ensure_space(_estimate_section_height(len(main_rows)))
        y = _draw_table(stream, main_rows, y, table_headers)
        if week_rows:
            y -= 8
            ensure_space(_estimate_section_height(len(week_rows)))
            y = _draw_table(stream, week_rows, y, week_table_headers)
        if pdf_adjustment_rows:
            y -= 8
            ensure_space(_estimate_section_height(len(pdf_adjustment_rows)))
            y = _draw_table(stream, pdf_adjustment_rows, y, week_table_headers)
        y -= 8
        ensure_space(110)
        _rect(stream, margin, y - total_box_height, left_total_width, total_box_height, (1.0, 0.973, 0.710))
        _rect(stream, margin + left_total_width, y - total_box_height, right_total_width, total_box_height, (1.0, 0.973, 0.710))
        _text(stream, margin + 8, y - 12, "TOTAL", size=10, font="F2")
        _text(stream, margin + left_total_width + 8, y - 12, _format_peso_number(final_total), size=10, font="F2")
        y -= total_box_height + 10
        y -= 10
        for line in RECEIPT_LINES:
            _text(stream, margin + 2, y, line, size=10, font="F1")
            y -= 14
        y -= 32
        signature_y = max(y, margin + 28)
        _line(stream, margin, signature_y, margin + left_signature_width, signature_y)
        _line(stream, page_width - margin - right_signature_width, signature_y, page_width - margin, signature_y)
        _text(stream, margin + 6, signature_y - 16, "FIRMA EMPLEADOR", size=10, font="F1")
        _text(stream, page_width - margin - right_signature_width + 6, signature_y - 16, "FIRMA TRABAJADOR", size=10, font="F1")
        pages.append("\n".join(stream))

    objects: list[bytes] = []

    def add_object(payload: bytes) -> int:
        objects.append(payload)
        return len(objects)

    font_regular_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    font_bold_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    image_id = None
    if logo_bytes:
        logo_width_px, logo_height_px = _jpeg_dimensions(logo_bytes)
        image_id = add_object(
            (
                f"<< /Type /XObject /Subtype /Image /Width {logo_width_px} /Height {logo_height_px} "
                f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length {len(logo_bytes)} >>\nstream\n"
            ).encode("latin-1")
            + logo_bytes
            + b"\nendstream"
        )

    page_ids: list[int] = []
    content_ids: list[int] = []
    pages_tree_id = 0
    for page_stream in pages:
        stream_bytes = page_stream.encode("latin-1", "replace")
        content_id = add_object(
            f"<< /Length {len(stream_bytes)} >>\nstream\n".encode("latin-1")
            + stream_bytes
            + b"\nendstream"
        )
        content_ids.append(content_id)
        page_ids.append(0)

    pages_tree_id = add_object(b"")
    for index, content_id in enumerate(content_ids):
        page_payload = (
            f"<< /Type /Page /Parent {pages_tree_id} 0 R "
            f"/MediaBox [0 0 {page_width} {page_height}] "
            f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> "
            + (f"/XObject << /Im1 {image_id} 0 R >> " if image_id else "")
            + ">> "
            f"/Contents {content_id} 0 R >>"
        ).encode("latin-1")
        page_ids[index] = add_object(page_payload)

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[pages_tree_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin-1")
    catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_tree_id} 0 R >>".encode("latin-1"))

    output = BytesIO()
    output.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for object_id, payload in enumerate(objects, start=1):
        offsets.append(output.tell())
        output.write(f"{object_id} 0 obj\n".encode("latin-1"))
        output.write(payload)
        output.write(b"\nendobj\n")
    xref_offset = output.tell()
    output.write(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    output.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode("latin-1"))
    output.write(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF"
        ).encode("latin-1")
    )
    return output.getvalue()


def export_sheet_pdf_bytes(settlement: dict[str, object]) -> bytes:
    """Export the complete on-screen payroll grid on one page sized to its content."""
    dates = settlement["dates"]
    rows = settlement["rows"]
    statuses = settlement["statuses"]
    column_widths = [220, 62, 72, 82] + [58] * len(dates)
    margin = 18
    header_heights = (40, 20, 30)
    row_height = 20
    page_width = sum(column_widths) + margin * 2
    page_height = margin * 2 + sum(header_heights) + row_height * len(rows)
    stream = ["0.7 w", "0 0 0 RG", "0 0 0 rg"]

    def latin(value: object) -> str:
        text = str(value or "").replace("—", "-").replace("–", "-").replace("…", "...")
        text = text.encode("cp1252", "replace").decode("cp1252")
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def cell_text(value: object, width: int) -> str:
        maximum = max(3, int((width - 6) / 5.2))
        text = str(value or "")
        return text if len(text) <= maximum else f"{text[:maximum - 1]}…"

    def draw_row(values: list[object], top: float, height: float, *, blue: bool = False, bold: bool = False) -> None:
        x = margin
        if blue:
            stream.append("0.741 0.843 0.933 rg")
            stream.append(f"{margin} {top - height} {sum(column_widths)} {height} re f")
            stream.append("0 0 0 rg")
        stream.append(f"{margin} {top - height} {sum(column_widths)} {height} re S")
        for index, width in enumerate(column_widths):
            if index:
                stream.append(f"{x} {top} m {x} {top - height} l S")
            value = values[index] if index < len(values) else ""
            font = "F2" if bold else "F1"
            text_lines = str(value or "").splitlines()[:2] or [""]
            for line_index, line in enumerate(text_lines):
                baseline = top - 12 - line_index * 11
                stream.append(
                    f"BT /{font} 8 Tf 1 0 0 1 {x + 3} {baseline} Tm "
                    f"({latin(cell_text(line, width))}) Tj ET"
                )
            x += width

    employee_name = settlement["employee"]["employee_name"]
    employee_rut = settlement["employee"].get("rut") or ""
    employee_heading = f"{employee_name}\nRUT: {employee_rut}" if employee_rut else employee_name
    y = page_height - margin
    draw_row(
        [
            employee_heading,
            "Unidades",
            "Tarifa",
            "Total $",
        ]
        + [item["label"] for item in dates],
        y,
        header_heights[0],
        blue=True,
        bold=True,
    )
    y -= header_heights[0]
    draw_row(
        ["", "", "", ""] + [PDF_WEEKDAY_LABELS.get(item["weekday"], item["weekday"]) for item in dates],
        y,
        header_heights[1],
        blue=True,
        bold=True,
    )
    y -= header_heights[1]
    draw_row(
        ["Estado", "", "", ""] + [_format_status_label(item.get("status")) for item in statuses],
        y,
        header_heights[2],
        blue=True,
        bold=True,
    )
    y -= header_heights[2]
    for row in rows:
        daily_values = [item.get("value") for item in row["daily_values"]]
        draw_row(
            [
                row["concept_name"],
                _format_peso_number(row.get("units")),
                _format_peso_number(row.get("rate")),
                _format_peso_number(row.get("total")),
            ] + [_format_peso_number(value) for value in daily_values],
            y,
            row_height,
            blue=row["row_type"] in {"total_to_pay", "variable_daily", "worked_day", "week_corrida", "production_total"},
            bold=row["row_type"] in {"total_to_pay", "production_total"},
        )
        y -= row_height

    stream_bytes = "\n".join(stream).encode("latin-1", "replace")
    objects = [
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
        f"<< /Length {len(stream_bytes)} >>\nstream\n".encode("latin-1") + stream_bytes + b"\nendstream",
        b"",
        b"",
    ]
    objects[3] = (
        f"<< /Type /Page /Parent 5 0 R /MediaBox [0 0 {page_width} {page_height}] "
        f"/Resources << /Font << /F1 1 0 R /F2 2 0 R >> >> /Contents 3 0 R >>"
    ).encode("latin-1")
    objects[4] = b"<< /Type /Pages /Kids [4 0 R] /Count 1 >>"
    objects.append(b"<< /Type /Catalog /Pages 5 0 R >>")
    output = BytesIO()
    output.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for object_id, payload in enumerate(objects, start=1):
        offsets.append(output.tell())
        output.write(f"{object_id} 0 obj\n".encode("latin-1"))
        output.write(payload)
        output.write(b"\nendobj\n")
    xref_offset = output.tell()
    output.write(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    output.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode("latin-1"))
    output.write(
        f"trailer\n<< /Size {len(objects) + 1} /Root 6 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode("latin-1")
    )
    return output.getvalue()


def export_file_name(
    *,
    settlement: dict[str, object],
    file_format: str,
    cost_center: str | None,
    role_type: str | None,
) -> str:
    employee = _file_component(settlement["employee"]["employee_name"])
    cycle_month = _file_component(_cycle_file_month(settlement["cycle"]["cycle_name"]))
    return f"{employee}-{cycle_month}.{file_format}"


def export_softland_file_name(settlement: dict[str, object], file_format: str = "xlsx") -> str:
    employee = _file_component(settlement["employee"]["employee_name"])
    cycle_month = _file_component(_cycle_file_month(settlement["cycle"]["cycle_name"]))
    return f"SL-{employee}-{cycle_month}.{file_format}"
