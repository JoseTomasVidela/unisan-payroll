from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
import unicodedata

from sqlalchemy import and_, func, or_, select, tuple_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .holidays import HolidayService
from .models import (
    PayrollCellOverride,
    Employee,
    PayrollConcept,
    PayrollAuditLog,
    PayrollCycle,
    PayrollManualAdjustment,
    PayrollRecord,
)
from .employee_names import names_refer_to_same_person, normalize_employee_name
from .rates import ConceptRateService
from .week_corrida import WeekCorridaCalculator

ZERO = Decimal("0")
RESERVED_RECORD_FIELDS = {"retrieval_flag", "septic_tank_flag"}
NON_CONCEPT_RECORD_FIELDS = {
    "id",
    "cycle_id",
    "import_id",
    "employee_id",
    "source_type",
    "cost_center",
    "role_type",
    "source_employee_name",
    "source_employee_code",
    "source_row_number",
    "source_row_hash",
    "source_person_slot",
    "work_date",
    "duration_minutes",
    "status",
}
WEEKDAY_LABELS = ("lun", "mar", "mie", "jue", "vie", "sab", "dom")
PRODUCTION_ADJUSTMENT_TYPES = {
    "VACATION",
    "OUT_OF_PRODUCTION_BONUS",
    "BONUS",
    "MANUAL_ADJUSTMENT",
}
ADJUSTMENT_ROW_ORDER = [
    ("VACATION", "VACACIONES"),
    ("OUT_OF_PRODUCTION_BONUS", "BONO FUERA DE PRODUCCION"),
    ("BONUS", "BONOS"),
    ("MANUAL_ADJUSTMENT", "AJUSTE MANUAL"),
    ("DISCOUNT", "DESCUENTOS"),
]
WORKED_DAY_ZERO_STATUSES = {
    "licencia",
    "vacaciones",
    "libre compensatorio",
    "descanso",
}
WORKED_DAY_ONE_STATUSES = {
    "sin produccion",
    "inasistencia",
}
EDITABLE_STATUSES = {
    "licencia": "Licencia",
    "vacaciones": "Vacaciones",
    "libre compensatorio": "Libre compensatorio",
    "descanso": "Descanso",
    "feriado": "Feriado",
    "inasistencia": "Inasistencia",
    "sin produccion": "Sin producción",
}


def inclusive_dates(start_date: date, end_date: date) -> list[date]:
    if end_date < start_date:
        raise ValueError("El ciclo tiene un rango de fechas invalido.")
    return [
        start_date + timedelta(days=offset)
        for offset in range((end_date - start_date).days + 1)
    ]


def concept_record_fields() -> set[str]:
    return {
        column.name
        for column in PayrollRecord.__table__.columns
        if column.name not in NON_CONCEPT_RECORD_FIELDS | RESERVED_RECORD_FIELDS
    }


class ConceptRateProvider:
    def __init__(self, service: ConceptRateService | None = None) -> None:
        self.service = service or ConceptRateService()

    def active_rates(
        self,
        db: Session,
        concept_ids: list[int],
        cycle_id: int,
        contract_type: str | None = None,
    ):
        return self.service.effective_rates(
            db,
            concept_ids=concept_ids,
            cycle_id=cycle_id,
            contract_type=contract_type,
        )


class SettlementEngine:
    def __init__(
        self,
        rate_provider: ConceptRateProvider | None = None,
        week_corrida_calculator: WeekCorridaCalculator | None = None,
        holiday_service: HolidayService | None = None,
    ) -> None:
        self.rate_provider = rate_provider or ConceptRateProvider()
        self.week_corrida_calculator = week_corrida_calculator or WeekCorridaCalculator()
        self.holiday_service = holiday_service or HolidayService()

    def list_employees(
        self,
        db: Session,
        *,
        cycle_id: int,
        cost_center: str,
        role_type: str,
    ) -> list[Employee]:
        employees = list(
            db.scalars(
                select(Employee)
                .join(PayrollRecord, PayrollRecord.employee_id == Employee.id)
                .where(
                    PayrollRecord.cycle_id == cycle_id,
                    PayrollRecord.cost_center == cost_center,
                    PayrollRecord.role_type == role_type,
                )
                .order_by(Employee.id)
            ).all()
        )
        grouped: dict[str, list[Employee]] = {}
        for employee in employees:
            key = normalize_employee_name(employee.employee_name)
            grouped.setdefault(key, []).append(employee)
        results = []
        for matches in grouped.values():
            worker = min(matches, key=lambda item: item.id)
            results.append(
                Employee(
                    id=worker.id,
                    employee_name=worker.employee_name,
                    role_type=role_type,
                    contract_type=next((item.contract_type for item in matches if item.contract_type), None),
                    rut=next((item.rut for item in matches if item.rut), None),
                    email=next((item.email for item in matches if item.email), None),
                    cargo=next((item.cargo for item in matches if item.cargo), None),
                )
            )
        return sorted(results, key=lambda item: item.employee_name)

    def build(
        self,
        db: Session,
        *,
        cycle_id: int,
        employee_id: int,
        cost_center: str | None,
        role_type: str | None,
    ) -> dict[str, object]:
        if cost_center is None or role_type is None:
            return self._build_consolidated(
                db,
                cycle_id=cycle_id,
                employee_id=employee_id,
            )
        return self._build_context(
            db,
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=cost_center,
            role_type=role_type,
        )

    def _build_context(
        self,
        db: Session,
        *,
        cycle_id: int,
        employee_id: int,
        cost_center: str,
        role_type: str,
    ) -> dict[str, object]:
        cycle = db.get(PayrollCycle, cycle_id)
        if cycle is None:
            raise LookupError("Ciclo no encontrado.")
        employee = db.get(Employee, employee_id)
        if employee is None:
            raise LookupError("Trabajador no encontrado.")
        related_employees = list(
            db.scalars(
                select(Employee).order_by(Employee.id)
            ).all()
        )
        related_employees = [
            item for item in related_employees if names_refer_to_same_person(item.employee_name, employee.employee_name)
        ]
        employee_ids = [item.id for item in related_employees]
        contract_type = next(
            (item.contract_type for item in related_employees if item.contract_type),
            employee.contract_type,
        )
        records = list(
            db.scalars(
                select(PayrollRecord)
                .where(
                    PayrollRecord.cycle_id == cycle_id,
                    PayrollRecord.employee_id.in_(employee_ids),
                    PayrollRecord.cost_center == cost_center,
                    PayrollRecord.role_type == role_type,
                )
                .order_by(PayrollRecord.work_date, PayrollRecord.id)
            ).all()
        )
        if not records:
            raise LookupError("No existen registros para la liquidacion seleccionada.")

        concepts = list(
            db.scalars(
                select(PayrollConcept)
                .where(
                    PayrollConcept.cost_center == cost_center,
                    PayrollConcept.role_type == role_type,
                    PayrollConcept.active.is_(True),
                )
                .order_by(PayrollConcept.display_order, PayrollConcept.id)
            ).all()
        )
        dates = inclusive_dates(cycle.start_date, cycle.end_date)
        records_by_date: dict[date, list[PayrollRecord]] = defaultdict(list)
        for record in records:
            records_by_date[record.work_date].append(record)

        overrides_by_key = self._load_cell_overrides(
            db,
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=cost_center,
            role_type=role_type,
        )
        adjustments = list(
            db.scalars(
                select(PayrollManualAdjustment).where(
                    PayrollManualAdjustment.cycle_id == cycle_id,
                    PayrollManualAdjustment.employee_id == employee_id,
                    or_(
                        and_(
                            PayrollManualAdjustment.cost_center == cost_center,
                            PayrollManualAdjustment.role_type == role_type,
                        ),
                        and_(
                            PayrollManualAdjustment.cost_center == "ALL",
                            PayrollManualAdjustment.role_type == "ALL",
                        ),
                    ),
                    PayrollManualAdjustment.active.is_(True),
                )
            ).all()
        )
        rates = self.rate_provider.active_rates(
            db,
            [concept.id for concept in concepts],
            cycle_id,
            contract_type=contract_type,
        )
        rows, variable_daily = self._build_rows_for_concepts(
            concepts=concepts,
            dates=dates,
            overrides_by_key=overrides_by_key,
            value_loader=lambda concept, work_date: sum(
                (
                    getattr(record, concept.db_field) or ZERO
                    for record in records_by_date.get(work_date, [])
                ),
                ZERO,
            ),
            rates=rates,
            include_empty=True,
            display_name=lambda concept: concept.concept_name,
        )
        statuses = []
        worked_day: dict[date, Decimal] = {}
        for work_date in dates:
            status = next(
                (
                    record.status
                    for record in records_by_date.get(work_date, [])
                    if record.status and record.status.strip()
                ),
                None,
            )
            statuses.append({"date": work_date, "status": status})
            worked_day[work_date] = self._worked_day_value(
                status=status,
                variable_amount=variable_daily[work_date],
            )
        self._apply_cycle_start_worked_day_offset(
            worked_day=worked_day,
            cycle_start_date=cycle.start_date,
        )
        return self._response_payload(
            db=db,
            employee=employee,
            contract_type=contract_type,
            cycle=cycle,
            cost_center=cost_center,
            role_type=role_type,
            dates=dates,
            statuses=statuses,
            rows=rows,
            variable_daily=variable_daily,
            worked_day=worked_day,
            adjustments=adjustments,
        )

    def _build_consolidated(
        self,
        db: Session,
        *,
        cycle_id: int,
        employee_id: int,
    ) -> dict[str, object]:
        cycle = db.get(PayrollCycle, cycle_id)
        if cycle is None:
            raise LookupError("Ciclo no encontrado.")
        employee = db.get(Employee, employee_id)
        if employee is None:
            raise LookupError("Trabajador no encontrado.")
        related_employees = list(
            db.scalars(
                select(Employee).order_by(Employee.id)
            ).all()
        )
        related_employees = [
            item for item in related_employees if names_refer_to_same_person(item.employee_name, employee.employee_name)
        ]
        employee_ids = [item.id for item in related_employees]
        contract_type = next(
            (item.contract_type for item in related_employees if item.contract_type),
            employee.contract_type,
        )
        records = list(
            db.scalars(
                select(PayrollRecord)
                .where(
                    PayrollRecord.cycle_id == cycle_id,
                    PayrollRecord.employee_id.in_(employee_ids),
                )
                .order_by(
                    PayrollRecord.cost_center,
                    PayrollRecord.role_type,
                    PayrollRecord.work_date,
                    PayrollRecord.id,
                )
            ).all()
        )
        if not records:
            raise LookupError("No existen registros para la liquidacion seleccionada.")

        override_rows = list(
            db.scalars(
                select(PayrollCellOverride).where(
                    PayrollCellOverride.cycle_id == cycle_id,
                    PayrollCellOverride.employee_id == employee_id,
                )
            ).all()
        )
        context_pairs = sorted(
            {
                *((record.cost_center, record.role_type) for record in records),
                *((override.cost_center, override.role_type) for override in override_rows),
            }
        )
        concepts = list(
            db.scalars(
                select(PayrollConcept)
                .where(
                    PayrollConcept.active.is_(True),
                    tuple_(PayrollConcept.cost_center, PayrollConcept.role_type).in_(context_pairs),
                )
                .order_by(
                    PayrollConcept.cost_center,
                    PayrollConcept.role_type,
                    PayrollConcept.display_order,
                    PayrollConcept.id,
                )
            ).all()
        )
        dates = inclusive_dates(cycle.start_date, cycle.end_date)
        records_by_context_date: dict[tuple[str, str, date], list[PayrollRecord]] = defaultdict(list)
        for record in records:
            records_by_context_date[(record.cost_center, record.role_type, record.work_date)].append(record)

        overrides_by_key = {
            (override.concept_id, override.work_date): override.override_value
            for override in override_rows
        }
        adjustments = list(
            db.scalars(
                select(PayrollManualAdjustment).where(
                    PayrollManualAdjustment.cycle_id == cycle_id,
                    PayrollManualAdjustment.employee_id.in_(employee_ids),
                    PayrollManualAdjustment.active.is_(True),
                )
            ).all()
        )
        rates = self.rate_provider.active_rates(
            db,
            [concept.id for concept in concepts],
            cycle_id,
            contract_type=contract_type,
        )
        rows, variable_daily = self._build_rows_for_concepts(
            concepts=concepts,
            dates=dates,
            overrides_by_key=overrides_by_key,
            value_loader=lambda concept, work_date: sum(
                (
                    getattr(record, concept.db_field) or ZERO
                    for record in records_by_context_date.get(
                        (concept.cost_center, concept.role_type, work_date), []
                    )
                ),
                ZERO,
            ),
            rates=rates,
            include_empty=False,
            display_name=self._display_name_for_concept,
        )
        statuses = []
        worked_day: dict[date, Decimal] = {}
        for work_date in dates:
            day_statuses = sorted(
                {
                    record.status.strip()
                    for record in records
                    if record.work_date == work_date and record.status and record.status.strip()
                }
            )
            status = " / ".join(day_statuses) if day_statuses else None
            statuses.append({"date": work_date, "status": status})
            worked_day[work_date] = self._worked_day_value(
                status=status,
                variable_amount=variable_daily[work_date],
            )
        self._apply_cycle_start_worked_day_offset(
            worked_day=worked_day,
            cycle_start_date=cycle.start_date,
        )
        return self._response_payload(
            db=db,
            employee=employee,
            contract_type=contract_type,
            cycle=cycle,
            cost_center=None,
            role_type=None,
            dates=dates,
            statuses=statuses,
            rows=rows,
            variable_daily=variable_daily,
            worked_day=worked_day,
            adjustments=adjustments,
        )

    def _build_rows_for_concepts(
        self,
        *,
        concepts: list[PayrollConcept],
        dates: list[date],
        overrides_by_key: dict[tuple[int, date], Decimal],
        value_loader,
        rates,
        include_empty: bool,
        display_name,
    ) -> tuple[list[dict[str, object]], dict[date, Decimal]]:
        valid_fields = concept_record_fields()
        invalid_fields = sorted(
            {concept.db_field for concept in concepts if concept.db_field not in valid_fields}
        )
        if invalid_fields:
            raise ValueError(
                "Conceptos con db_field invalido o reservado: " + ", ".join(invalid_fields)
            )
        variable_daily = {work_date: ZERO for work_date in dates}
        rows: list[dict[str, object]] = []
        for concept in concepts:
            daily_values: list[dict[str, object]] = []
            units = ZERO
            has_activity = False
            rate_version = rates.get(concept.id)
            rate = rate_version.amount if rate_version else ZERO
            for work_date in dates:
                value = overrides_by_key.get((concept.id, work_date))
                if value is None:
                    value = value_loader(concept, work_date)
                if value != ZERO:
                    has_activity = True
                units += value
                variable_daily[work_date] += value * rate
                daily_values.append({"date": work_date, "value": value, "editable": False})
            if not include_empty and not has_activity:
                continue
            rows.append(
                {
                    "row_type": "concept",
                    "concept_id": concept.id,
                    "rate_id": rate_version.id if rate_version else None,
                    "concept_code": concept.concept_code,
                    "concept_name": display_name(concept),
                    "db_field": concept.db_field,
                    "units": units,
                    "rate": rate,
                    "total": units * rate,
                    "editable": True,
                    "daily_values": daily_values,
                }
            )
        return rows, variable_daily

    def _response_payload(
        self,
        *,
        db: Session,
        employee: Employee,
        contract_type: str | None,
        cycle: PayrollCycle,
        cost_center: str | None,
        role_type: str | None,
        dates: list[date],
        statuses: list[dict[str, object]],
        rows: list[dict[str, object]],
        variable_daily: dict[date, Decimal],
        worked_day: dict[date, Decimal],
        adjustments: list[PayrollManualAdjustment],
    ) -> dict[str, object]:
        holiday_map = self.holiday_service.active_holiday_map(
            db,
            cycle.start_date,
            cycle.end_date,
        )
        total_to_pay = sum((row["total"] for row in rows), ZERO)
        holiday_calculator = WeekCorridaCalculator(
            holiday_provider=lambda target_date: target_date in holiday_map
        )
        week_corrida_total, week_corrida_daily, _ = holiday_calculator.calculate(
            start_date=cycle.start_date,
            end_date=cycle.end_date,
            variable_daily=variable_daily,
            worked_day=worked_day,
        )
        adjustment_line_totals = {
            adjustment.id: (adjustment.units or Decimal("1")) * adjustment.amount
            for adjustment in adjustments
        }
        adjustments_total = sum(
            (
                adjustment_line_totals[adjustment.id]
                for adjustment in adjustments
                if adjustment.adjustment_type in PRODUCTION_ADJUSTMENT_TYPES
            ),
            ZERO,
        )
        discounts_total = sum(
            (
                adjustment_line_totals[adjustment.id]
                for adjustment in adjustments
                if adjustment.adjustment_type == "DISCOUNT"
            ),
            ZERO,
        )
        production_total = total_to_pay + week_corrida_total + adjustments_total - discounts_total
        adjustment_rows = [
            self._calculated_row(
                row_type=f"adjustment_{adjustment.adjustment_type.lower()}",
                concept_name=adjustment.adjustment_name,
                units=adjustment.units or Decimal("1"),
                rate=adjustment.amount,
                total=adjustment_line_totals[adjustment.id],
                daily_values={work_date: None for work_date in dates},
            )
            for adjustment in adjustments
            if adjustment_line_totals[adjustment.id] != ZERO
        ]
        rows = rows + [
            self._calculated_row(
                row_type="total_to_pay",
                concept_name="TOTAL A PAGAR",
                total=total_to_pay,
                daily_values={work_date: variable_daily[work_date] for work_date in dates},
            ),
            self._calculated_row(
                row_type="variable_daily",
                concept_name="VARIABLE DIARIO",
                total=None,
                daily_values={work_date: variable_daily[work_date] for work_date in dates},
            ),
            self._calculated_row(
                row_type="worked_day",
                concept_name="DIA TRABAJADO",
                total=None,
                daily_values=worked_day,
            ),
            self._calculated_row(
                row_type="week_corrida",
                concept_name="SEMANA CORRIDA",
                total=week_corrida_total,
                daily_values=week_corrida_daily,
            ),
            *adjustment_rows,
            self._calculated_row(
                row_type="production_total",
                concept_name="PRODUCCION TOTAL",
                total=production_total,
                daily_values={work_date: None for work_date in dates},
            ),
        ]
        return {
            "employee": {
                "id": employee.id,
                "employee_name": employee.employee_name,
                "contract_type": contract_type,
                "rut": employee.rut,
                "email": employee.email,
                "cargo": employee.cargo,
            },
            "cycle": {
                "id": cycle.id,
                "cycle_name": cycle.cycle_name,
                "start_date": cycle.start_date,
                "end_date": cycle.end_date,
            },
            "cost_center": cost_center,
            "role_type": role_type,
            "dates": [
                {
                    "date": work_date,
                    "label": work_date.strftime("%d-%m"),
                    "weekday": WEEKDAY_LABELS[work_date.weekday()],
                    "is_holiday": work_date in holiday_map,
                    "holiday_names": holiday_map.get(work_date, []),
                }
                for work_date in dates
            ],
            "statuses": statuses,
            "rows": rows,
            "daily_totals": [
                {"date": work_date, "value": variable_daily[work_date]}
                for work_date in dates
            ],
            "total_to_pay": total_to_pay,
            "week_corrida": week_corrida_total,
            "production_total": production_total,
        }

    def update_daily_cells(
        self,
        db: Session,
        *,
        cycle_id: int,
        employee_id: int,
        cost_center: str | None,
        role_type: str | None,
        updates: list[tuple[int, date, Decimal]],
        user_id: int,
    ) -> dict[str, object]:
        valid_fields = concept_record_fields()
        cycle = db.get(PayrollCycle, cycle_id)
        if cycle is None:
            raise LookupError("Ciclo no encontrado.")
        employee = db.get(Employee, employee_id)
        if employee is None:
            raise LookupError("Trabajador no encontrado.")
        related_employee_ids = [item.id for item in db.scalars(select(Employee).order_by(Employee.id)).all()
                                if names_refer_to_same_person(item.employee_name, employee.employee_name)]
        try:
            for concept_id, work_date, value in updates:
                concept = db.get(PayrollConcept, concept_id)
                if concept is None:
                    raise LookupError("Concepto no encontrado.")
                if (
                    cost_center is not None
                    and role_type is not None
                    and (concept.cost_center != cost_center or concept.role_type != role_type)
                ):
                    raise ValueError("El concepto no pertenece a la liquidacion actual.")
                if concept.db_field not in valid_fields:
                    raise ValueError("El concepto apunta a un campo reservado o invalido.")
                if work_date < cycle.start_date or work_date > cycle.end_date:
                    raise ValueError("La fecha no pertenece al ciclo seleccionado.")
                records = list(
                    db.scalars(
                        select(PayrollRecord)
                        .where(
                            PayrollRecord.cycle_id == cycle_id,
                            PayrollRecord.employee_id.in_(related_employee_ids),
                            PayrollRecord.cost_center == concept.cost_center,
                            PayrollRecord.role_type == concept.role_type,
                            PayrollRecord.work_date == work_date,
                        )
                        .order_by(PayrollRecord.id)
                    ).all()
                )
                if not records:
                    has_context_records = db.scalar(
                        select(func.count(PayrollRecord.id)).where(
                            PayrollRecord.cycle_id == cycle_id,
                            PayrollRecord.employee_id.in_(related_employee_ids),
                            PayrollRecord.cost_center == concept.cost_center,
                            PayrollRecord.role_type == concept.role_type,
                        )
                    )
                    if not has_context_records:
                        has_cycle_records = db.scalar(
                            select(func.count(PayrollRecord.id)).where(
                                PayrollRecord.cycle_id == cycle_id,
                                PayrollRecord.employee_id.in_(related_employee_ids),
                            )
                        )
                        if cost_center is not None or role_type is not None or not has_cycle_records:
                            raise LookupError("No existen registros base para la actividad seleccionada.")
                existing_override = db.scalar(
                    select(PayrollCellOverride)
                    .where(
                        PayrollCellOverride.cycle_id == cycle_id,
                        PayrollCellOverride.employee_id == employee_id,
                        PayrollCellOverride.concept_id == concept_id,
                        PayrollCellOverride.cost_center == concept.cost_center,
                        PayrollCellOverride.role_type == concept.role_type,
                        PayrollCellOverride.work_date == work_date,
                    )
                    .order_by(PayrollCellOverride.id.desc())
                )
                if existing_override is not None:
                    old_value = existing_override.override_value
                else:
                    old_value = sum(
                        (getattr(record, concept.db_field) or ZERO for record in records),
                        ZERO,
                    )
                if old_value == value:
                    continue
                if existing_override is None:
                    override = PayrollCellOverride(
                        cycle_id=cycle_id,
                        employee_id=employee_id,
                        concept_id=concept_id,
                        cost_center=concept.cost_center,
                        role_type=concept.role_type,
                        work_date=work_date,
                        override_value=value,
                        created_by=user_id,
                    )
                    db.add(override)
                    db.flush()
                    record_id = override.id
                else:
                    existing_override.override_value = value
                    record_id = existing_override.id
                db.add(
                    PayrollAuditLog(
                        user_id=user_id,
                        action_type="UPDATE_DAILY_CELL_OVERRIDE",
                        table_name="payroll_cell_overrides",
                        record_id=record_id,
                        field_name="override_value",
                        old_value=str(old_value),
                        new_value=str(value),
                    )
                )
        except SQLAlchemyError as exc:
            raise ValueError(
                "El esquema actual no soporta overrides manuales de celdas."
            ) from exc
        db.flush()
        return self.build(
            db,
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=cost_center,
            role_type=role_type,
        )

    def update_daily_statuses(
        self,
        db: Session,
        *,
        cycle_id: int,
        employee_id: int,
        cost_center: str | None,
        role_type: str | None,
        updates: list[tuple[date, str]],
        user_id: int,
    ) -> dict[str, object]:
        cycle = db.get(PayrollCycle, cycle_id)
        if cycle is None:
            raise LookupError("Ciclo no encontrado.")
        employee = db.get(Employee, employee_id)
        if employee is None:
            raise LookupError("Trabajador no encontrado.")
        related_employee_ids = [
            item.id
            for item in db.scalars(select(Employee).order_by(Employee.id)).all()
            if names_refer_to_same_person(item.employee_name, employee.employee_name)
        ]
        for work_date, status in updates:
            if work_date < cycle.start_date or work_date > cycle.end_date:
                raise ValueError("La fecha no pertenece al ciclo seleccionado.")
            normalized_status = self._normalize_status(status)
            if normalized_status not in EDITABLE_STATUSES:
                raise ValueError("Estado de liquidación inválido.")
            canonical_status = EDITABLE_STATUSES[normalized_status]
            filters = [
                PayrollRecord.cycle_id == cycle_id,
                PayrollRecord.employee_id.in_(related_employee_ids),
                PayrollRecord.work_date == work_date,
            ]
            if cost_center is not None:
                filters.append(PayrollRecord.cost_center == cost_center)
            if role_type is not None:
                filters.append(PayrollRecord.role_type == role_type)
            records = list(
                db.scalars(select(PayrollRecord).where(*filters).order_by(PayrollRecord.id)).all()
            )
            if not records:
                raise LookupError("No existen registros para cambiar el estado de esa fecha.")
            for record in records:
                old_value = record.status
                if old_value == canonical_status:
                    continue
                record.status = canonical_status
                db.add(
                    PayrollAuditLog(
                        user_id=user_id,
                        action_type="UPDATE_DAILY_STATUS",
                        table_name="payroll_records",
                        record_id=record.id,
                        field_name="status",
                        old_value=old_value,
                        new_value=canonical_status,
                    )
                )
        db.flush()
        return self.build(
            db,
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=cost_center,
            role_type=role_type,
        )

    def _load_cell_overrides(
        self,
        db: Session,
        *,
        cycle_id: int,
        employee_id: int,
        cost_center: str,
        role_type: str,
    ) -> dict[tuple[int, date], Decimal]:
        try:
            rows = db.scalars(
                select(PayrollCellOverride)
                .where(
                    PayrollCellOverride.cycle_id == cycle_id,
                    PayrollCellOverride.employee_id == employee_id,
                    PayrollCellOverride.cost_center == cost_center,
                    PayrollCellOverride.role_type == role_type,
                )
                .order_by(PayrollCellOverride.id.desc())
            ).all()
        except SQLAlchemyError:
            return {}
        overrides: dict[tuple[int, date], Decimal] = {}
        for row in rows:
            overrides.setdefault((row.concept_id, row.work_date), row.override_value)
        return overrides

    @staticmethod
    def _display_name_for_concept(concept: PayrollConcept) -> str:
        center_label = "D&R" if concept.cost_center == "DR" else "Servicios"
        role_label = "Chofer" if concept.role_type == "DRIVER" else "Auxiliar"
        return f"{center_label} {role_label} - {concept.concept_name}"

    @staticmethod
    def _worked_day_value(
        *,
        status: str | None,
        variable_amount: Decimal,
    ) -> Decimal:
        normalized_status = SettlementEngine._normalize_status(status)
        if normalized_status in WORKED_DAY_ZERO_STATUSES:
            return ZERO
        if normalized_status in WORKED_DAY_ONE_STATUSES:
            return Decimal("1")
        if variable_amount < Decimal("1"):
            return ZERO
        return Decimal("1")

    @staticmethod
    def _normalize_status(status: str | None) -> str:
        raw_value = (status or "").strip().casefold()
        return "".join(
            character
            for character in unicodedata.normalize("NFKD", raw_value)
            if not unicodedata.combining(character)
        )

    @staticmethod
    def _apply_cycle_start_worked_day_offset(
        *,
        worked_day: dict[date, Decimal],
        cycle_start_date: date,
    ) -> None:
        if cycle_start_date not in worked_day:
            return
        weekday_offset = cycle_start_date.weekday()
        if weekday_offset <= 0:
            return
        worked_day[cycle_start_date] = worked_day[cycle_start_date] + Decimal(weekday_offset)

    @staticmethod
    def _calculated_row(
        *,
        row_type: str,
        concept_name: str,
        total: Decimal | None,
        daily_values: dict[date, Decimal | None],
        units: Decimal | None = None,
        rate: Decimal | None = None,
    ) -> dict[str, object]:
        return {
            "row_type": row_type,
            "concept_id": None,
            "rate_id": None,
            "concept_code": row_type.upper(),
            "concept_name": concept_name,
            "db_field": None,
            "units": units,
            "rate": rate,
            "total": total,
            "editable": False,
            "daily_values": [
                {"date": work_date, "value": value, "editable": False}
                for work_date, value in daily_values.items()
            ],
        }
