from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

ZERO = Decimal("0")


@dataclass(frozen=True)
class WeekCorridaSegment:
    start_date: date
    end_date: date
    payout_date: date
    payable_days: int
    amount: Decimal


def easter_sunday(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def chile_public_holidays(year: int) -> set[date]:
    easter = easter_sunday(year)
    return {
        date(year, 1, 1),
        easter - timedelta(days=2),  # Viernes Santo
        easter - timedelta(days=1),  # Sabado Santo
        date(year, 5, 1),
        date(year, 5, 21),
        date(year, 7, 16),
        date(year, 8, 15),
        date(year, 9, 18),
        date(year, 9, 19),
        date(year, 10, 31),
        date(year, 11, 1),
        date(year, 12, 8),
        date(year, 12, 25),
    }


def default_holiday_provider(target_date: date) -> bool:
    return target_date in chile_public_holidays(target_date.year)


class WeekCorridaCalculator:
    def __init__(
        self,
        holiday_provider: Callable[[date], bool] | None = None,
    ) -> None:
        self.holiday_provider = holiday_provider or default_holiday_provider

    def calculate(
        self,
        *,
        start_date: date,
        end_date: date,
        variable_daily: dict[date, Decimal],
        worked_day: dict[date, Decimal],
    ) -> tuple[Decimal, dict[date, Decimal | None], list[WeekCorridaSegment]]:
        if end_date < start_date:
            raise ValueError("El ciclo tiene un rango de fechas invalido.")

        segments = []
        segment_start = start_date
        while segment_start <= end_date:
            days_until_sunday = 6 - segment_start.weekday()
            segment_end = min(end_date, segment_start + timedelta(days=days_until_sunday))
            week_start = segment_start - timedelta(days=segment_start.weekday())
            week_end = week_start + timedelta(days=6)
            payable_range_start = segment_start if segment_start == start_date else week_start
            payable_days = sum(
                1
                for current_date in self._iter_dates(payable_range_start, week_end)
                if self._is_payable_day(current_date)
            )

            worked_total = sum(
                (worked_day.get(current_date, ZERO) for current_date in self._iter_dates(segment_start, segment_end)),
                ZERO,
            )
            variable_total = sum(
                (variable_daily.get(current_date, ZERO) for current_date in self._iter_dates(segment_start, segment_end)),
                ZERO,
            )
            amount = ZERO
            if worked_total > ZERO and payable_days > 0:
                amount = (variable_total / worked_total) * Decimal(payable_days)

            segments.append(
                WeekCorridaSegment(
                    start_date=segment_start,
                    end_date=segment_end,
                    payout_date=segment_end,
                    payable_days=payable_days,
                    amount=amount,
                )
            )
            segment_start = segment_end + timedelta(days=1)

        by_date = {current_date: None for current_date in self._iter_dates(start_date, end_date)}
        total = ZERO
        for segment in segments:
            by_date[segment.payout_date] = segment.amount
            total += segment.amount
        return total, by_date, segments

    def _is_payable_day(self, target_date: date) -> bool:
        return target_date.weekday() == 6 or self.holiday_provider(target_date)

    @staticmethod
    def _iter_dates(start_date: date, end_date: date):
        for offset in range((end_date - start_date).days + 1):
            yield start_date + timedelta(days=offset)
