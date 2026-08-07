from __future__ import annotations

import re
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.orm import Session

from .employee_names import normalize_employee_name
from .models import (
    Employee,
    PayrollConcept,
    PayrollCycle,
    PayrollManualAdjustment,
    PayrollRecord,
    PayrollSoftlandCode,
    PayrollSoftlandConceptMapping,
)

SOFTLAND_CODE_ORDER = ("H005", "H008", "H022", "H040")
SOFTLAND_CODES = {
    "H005": "SEMANA CORRIDA",
    "H008": "BONO RENDIMIENTO",
    "H022": "UNIBOX",
    "H040": "VACACIONES",
}
SPECIAL_MAPPINGS = {
    ("CALCULATED", "WEEK_CORRIDA"): ("SEMANA CORRIDA", "H005"),
    ("ADJUSTMENT", "OUT_OF_PRODUCTION_BONUS"): ("Bono fuera de producción", "H008"),
    ("ADJUSTMENT", "BONUS"): ("Bono", "H008"),
    ("ADJUSTMENT", "PRODUCTION_BONUS"): ("Bono Producción", "H008"),
    ("ADJUSTMENT", "VACATION_BONUS"): ("Bono Vacaciones", "H008"),
    ("ADJUSTMENT", "EVENT_BONUS"): ("Bono Evento", "H022"),
    ("ADJUSTMENT", "VACATION"): ("VACACIONES", "H040"),
}


def concept_mapping_key(concept: PayrollConcept) -> str:
    return "|".join(
        (concept.source_type, concept.cost_center, concept.role_type, concept.concept_code)
    )


def concept_softland_code(concept: PayrollConcept) -> str:
    if concept.concept_code in {
        "EVENT",
        "WATER_POINT",
        "LARGE_TRASH_BIN",
        "SMALL_TRASH_BIN",
        "FOSA",
    }:
        return "H022"
    return "H008"


def concept_source_label(concept: PayrollConcept) -> str:
    if concept.source_type == "DR" and concept.role_type == "ASSISTANT":
        return f"Aux {concept.concept_name}"
    if concept.source_type == "SERVICES" and concept.role_type == "DRIVER":
        return f"Servicio Chofer {concept.concept_name}"
    if concept.source_type == "SERVICES" and concept.role_type == "ASSISTANT":
        return f"Servicio Aux {concept.concept_name}"
    return concept.concept_name


def ensure_softland_mappings(db: Session) -> None:
    codes = {
        row.softland_code: row
        for row in db.scalars(select(PayrollSoftlandCode)).all()
    }
    for code, name in SOFTLAND_CODES.items():
        item = codes.get(code)
        if item is None:
            db.add(PayrollSoftlandCode(softland_code=code, concept_name=name))
        else:
            item.concept_name = name
            item.active = True
    db.flush()

    mappings = {
        (row.mapping_type, row.mapping_key): row
        for row in db.scalars(select(PayrollSoftlandConceptMapping)).all()
    }
    for concept in db.scalars(select(PayrollConcept).order_by(PayrollConcept.id)).all():
        key = ("CONCEPT", concept_mapping_key(concept))
        item = mappings.get(key)
        values = {
            "concept_id": concept.id,
            "source_label": concept_source_label(concept),
            "softland_code": concept_softland_code(concept),
        }
        if item is None:
            db.add(
                PayrollSoftlandConceptMapping(
                    mapping_type=key[0],
                    mapping_key=key[1],
                    active=True,
                    **values,
                )
            )
        else:
            for field, value in values.items():
                setattr(item, field, value)
            item.active = True

    for key, (label, code) in SPECIAL_MAPPINGS.items():
        item = mappings.get(key)
        if item is None:
            db.add(
                PayrollSoftlandConceptMapping(
                    concept_id=None,
                    mapping_type=key[0],
                    mapping_key=key[1],
                    source_label=label,
                    softland_code=code,
                    active=True,
                )
            )
        else:
            item.source_label = label
            item.softland_code = code
            item.active = True
    db.commit()


def softland_ficha(rut: str | None, employee_name: str) -> str:
    normalized = (rut or "").strip().upper()
    if not normalized:
        return employee_name.strip()
    body = normalized.rsplit("-", 1)[0] if "-" in normalized else normalized[:-1]
    digits = re.sub(r"\D", "", body)
    if not digits:
        raise ValueError(f"El RUT '{rut}' no tiene un formato válido.")
    return digits


def _employee_representatives(db: Session, cycle_id: int) -> list[Employee]:
    employees = list(
        db.scalars(
            select(Employee)
            .join(PayrollRecord, PayrollRecord.employee_id == Employee.id)
            .where(PayrollRecord.cycle_id == cycle_id)
            .order_by(Employee.id)
        ).unique().all()
    )
    grouped: dict[str, list[Employee]] = defaultdict(list)
    for employee in employees:
        grouped[normalize_employee_name(employee.employee_name)].append(employee)
    representatives = [
        next((employee for employee in matches if employee.rut), matches[0])
        for matches in grouped.values()
    ]
    return sorted(
        representatives,
        key=lambda item: (softland_ficha(item.rut, item.employee_name), item.id),
    )


def build_softland_rows(db: Session, *, cycle_id: int, settlement_engine) -> tuple[PayrollCycle, list[list[object]], list[int]]:
    cycle = db.get(PayrollCycle, cycle_id)
    if cycle is None:
        raise LookupError("Ciclo no encontrado.")

    concept_codes = {
        row.concept_id: row.softland_code
        for row in db.scalars(
            select(PayrollSoftlandConceptMapping).where(
                PayrollSoftlandConceptMapping.mapping_type == "CONCEPT",
                PayrollSoftlandConceptMapping.active.is_(True),
            )
        ).all()
        if row.concept_id is not None
    }
    special_codes = {
        (row.mapping_type, row.mapping_key): row.softland_code
        for row in db.scalars(
            select(PayrollSoftlandConceptMapping).where(
                PayrollSoftlandConceptMapping.mapping_type.in_(("CALCULATED", "ADJUSTMENT")),
                PayrollSoftlandConceptMapping.active.is_(True),
            )
        ).all()
    }
    employees = _employee_representatives(db, cycle_id)
    if not employees:
        raise LookupError("El ciclo no tiene trabajadores con registros para exportar.")

    month_year = cycle.end_date.strftime("%m/%Y")
    values_by_code: dict[str, list[list[object]]] = defaultdict(list)
    employee_ids: list[int] = []
    for employee in employees:
        ficha = softland_ficha(employee.rut, employee.employee_name)
        settlement = settlement_engine.build(
            db,
            cycle_id=cycle_id,
            employee_id=employee.id,
            cost_center=None,
            role_type=None,
        )
        totals = {code: Decimal("0") for code in SOFTLAND_CODE_ORDER}
        unmapped: list[str] = []
        for row in settlement["rows"]:
            total = Decimal(str(row.get("total") or 0))
            if total == 0:
                continue
            row_type = str(row["row_type"])
            code = None
            if row_type == "concept":
                code = concept_codes.get(row.get("concept_id"))
                if code is None:
                    unmapped.append(str(row.get("concept_name") or row.get("concept_code")))
            elif row_type == "week_corrida":
                code = special_codes.get(("CALCULATED", "WEEK_CORRIDA"))
            elif row_type.startswith("adjustment_"):
                adjustment_type = row_type.removeprefix("adjustment_").upper()
                code = special_codes.get(("ADJUSTMENT", adjustment_type))
                if code is None:
                    unmapped.append(str(row.get("concept_name") or adjustment_type))
            if code in totals:
                totals[code] += total
        if unmapped:
            raise ValueError(
                f"Conceptos sin homologación Softland para {employee.employee_name}: "
                + ", ".join(sorted(set(unmapped)))
            )
        employee_has_exported_value = False
        for code in SOFTLAND_CODE_ORDER:
            rounded = int(totals[code].quantize(Decimal("1"), rounding=ROUND_HALF_UP))
            if rounded == 0:
                continue
            values_by_code[code].append([ficha, code, month_year, rounded])
            employee_has_exported_value = True
        if employee_has_exported_value:
            employee_ids.append(employee.id)

    rows = [row for code in SOFTLAND_CODE_ORDER for row in values_by_code[code]]
    return cycle, rows, employee_ids
