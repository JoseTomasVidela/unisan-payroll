from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from sqlalchemy import extract, inspect, select
from sqlalchemy.orm import Session

from .models import PayrollHoliday
from .week_corrida import easter_sunday

HOLIDAY_SCOPE_CHILE = "CHILE"
HOLIDAY_SCOPE_WORLD = "WORLD"
HOLIDAY_SCOPE_CUSTOM = "CUSTOM"
ALLOWED_HOLIDAY_SCOPES = {
    HOLIDAY_SCOPE_CHILE,
    HOLIDAY_SCOPE_WORLD,
    HOLIDAY_SCOPE_CUSTOM,
}


@dataclass(frozen=True)
class DefaultHoliday:
    holiday_date: date
    holiday_name: str
    holiday_scope: str


def chile_default_holidays(year: int) -> list[DefaultHoliday]:
    easter = easter_sunday(year)
    return [
        DefaultHoliday(date(year, 1, 1), "Ano Nuevo", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(easter - date.resolution * 2, "Viernes Santo", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(easter - date.resolution, "Sabado Santo", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 5, 1), "Dia del Trabajador", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 5, 21), "Glorias Navales", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 7, 16), "Virgen del Carmen", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 8, 15), "Asuncion", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 9, 18), "Independencia Nacional", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 9, 19), "Glorias del Ejercito", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 10, 31), "Dia de las Iglesias Evangelicas", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 11, 1), "Dia de Todos los Santos", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 12, 8), "Inmaculada Concepcion", HOLIDAY_SCOPE_CHILE),
        DefaultHoliday(date(year, 12, 25), "Navidad", HOLIDAY_SCOPE_CHILE),
    ]


def world_default_holidays(year: int) -> list[DefaultHoliday]:
    return [
        DefaultHoliday(date(year, 1, 1), "New Year's Day", HOLIDAY_SCOPE_WORLD),
        DefaultHoliday(date(year, 5, 1), "International Workers' Day", HOLIDAY_SCOPE_WORLD),
        DefaultHoliday(date(year, 12, 25), "Christmas Day", HOLIDAY_SCOPE_WORLD),
    ]


def default_holidays_for_year(year: int) -> list[DefaultHoliday]:
    return [*chile_default_holidays(year), *world_default_holidays(year)]


class HolidayService:
    table_name = "payroll_holidays"

    def table_exists(self, db: Session) -> bool:
        return self.table_name in inspect(db.bind).get_table_names()

    def ensure_defaults(self, db: Session, year: int) -> None:
        if not self.table_exists(db):
            return
        default_rows = default_holidays_for_year(year)
        existing_keys = {
            (row.holiday_date, row.holiday_scope)
            for row in db.scalars(
                select(PayrollHoliday).where(extract("year", PayrollHoliday.holiday_date) == year)
            ).all()
        }
        missing = [
            PayrollHoliday(
                holiday_date=item.holiday_date,
                holiday_name=item.holiday_name,
                holiday_scope=item.holiday_scope,
                active=True,
                is_default=True,
                created_at=datetime.utcnow(),
            )
            for item in default_rows
            if (item.holiday_date, item.holiday_scope) not in existing_keys
        ]
        if missing:
            db.add_all(missing)
            db.flush()

    def list_month(self, db: Session, year: int, month: int) -> list[PayrollHoliday]:
        if not self.table_exists(db):
            return [
                PayrollHoliday(
                    id=0,
                    holiday_date=item.holiday_date,
                    holiday_name=item.holiday_name,
                    holiday_scope=item.holiday_scope,
                    active=True,
                    is_default=True,
                    created_at=datetime.utcnow(),
                )
                for item in default_holidays_for_year(year)
                if item.holiday_date.month == month
            ]
        self.ensure_defaults(db, year)
        return list(
            db.scalars(
                select(PayrollHoliday)
                .where(extract("year", PayrollHoliday.holiday_date) == year)
                .where(extract("month", PayrollHoliday.holiday_date) == month)
                .order_by(PayrollHoliday.holiday_date, PayrollHoliday.holiday_scope, PayrollHoliday.id)
            ).all()
        )

    def active_holiday_map(
        self,
        db: Session,
        start_date: date,
        end_date: date,
    ) -> dict[date, list[str]]:
        if start_date > end_date:
            return {}
        default_rows = [
            item
            for year in range(start_date.year, end_date.year + 1)
            for item in default_holidays_for_year(year)
            if start_date <= item.holiday_date <= end_date
        ]
        if not self.table_exists(db):
            holiday_map: dict[date, list[str]] = {}
            for item in default_rows:
                holiday_map.setdefault(item.holiday_date, []).append(item.holiday_name)
            return holiday_map

        rows = list(
            db.scalars(
                select(PayrollHoliday)
                .where(PayrollHoliday.holiday_date >= start_date)
                .where(PayrollHoliday.holiday_date <= end_date)
                .order_by(PayrollHoliday.holiday_date, PayrollHoliday.holiday_scope, PayrollHoliday.id)
            ).all()
        )
        rows_by_key = {
            (row.holiday_date, row.holiday_scope): row
            for row in rows
        }
        holiday_map: dict[date, list[str]] = {}
        for item in default_rows:
            row = rows_by_key.get((item.holiday_date, item.holiday_scope))
            if row is None:
                holiday_map.setdefault(item.holiday_date, []).append(item.holiday_name)
            elif row.active:
                holiday_map.setdefault(row.holiday_date, []).append(row.holiday_name)
        for row in rows:
            if row.holiday_scope == HOLIDAY_SCOPE_CUSTOM and row.active:
                holiday_map.setdefault(row.holiday_date, []).append(row.holiday_name)
        return holiday_map
