from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from app.week_corrida import WeekCorridaCalculator, monday_shifted_holiday


def build_daily_map(start_date: date, end_date: date, amount: Decimal) -> dict[date, Decimal]:
    return {
        start_date + timedelta(days=offset): amount
        for offset in range((end_date - start_date).days + 1)
    }


def test_week_corrida_matches_reference_cycle_pattern():
    calculator = WeekCorridaCalculator()
    start_date = date(2026, 4, 22)
    end_date = date(2026, 5, 21)
    variable_daily = build_daily_map(start_date, end_date, Decimal("10"))
    worked_day = build_daily_map(start_date, end_date, Decimal("1"))

    total, by_date, segments = calculator.calculate(
        start_date=start_date,
        end_date=end_date,
        variable_daily=variable_daily,
        worked_day=worked_day,
    )

    assert len(segments) == 5
    assert [segment.payout_date for segment in segments] == [
        date(2026, 4, 26),
        date(2026, 5, 3),
        date(2026, 5, 10),
        date(2026, 5, 17),
        date(2026, 5, 21),
    ]
    assert [segment.payable_days for segment in segments] == [1, 2, 1, 1, 2]
    assert [segment.amount for segment in segments] == [
        Decimal("10"),
        Decimal("20"),
        Decimal("10"),
        Decimal("10"),
        Decimal("20"),
    ]
    assert total == Decimal("70")
    assert by_date[date(2026, 5, 3)] == Decimal("20")
    assert by_date[date(2026, 5, 21)] == Decimal("20")
    assert by_date[date(2026, 4, 22)] is None


def test_week_corrida_returns_zero_when_no_worked_days():
    calculator = WeekCorridaCalculator()
    start_date = date(2026, 5, 22)
    end_date = date(2026, 6, 21)
    variable_daily = build_daily_map(start_date, end_date, Decimal("50"))
    worked_day = build_daily_map(start_date, end_date, Decimal("0"))

    total, by_date, segments = calculator.calculate(
        start_date=start_date,
        end_date=end_date,
        variable_daily=variable_daily,
        worked_day=worked_day,
    )

    assert total == Decimal("0")
    assert all(segment.amount == Decimal("0") for segment in segments)
    assert all(value in (None, Decimal("0")) for value in by_date.values())


def test_october_12_counts_as_payable_holiday_in_2026():
    calculator = WeekCorridaCalculator()
    start_date = date(2026, 10, 12)
    end_date = date(2026, 10, 18)

    total, _, segments = calculator.calculate(
        start_date=start_date,
        end_date=end_date,
        variable_daily=build_daily_map(start_date, end_date, Decimal("10")),
        worked_day=build_daily_map(start_date, end_date, Decimal("1")),
    )

    assert segments[0].payable_days == 2
    assert total == Decimal("20")


def test_legal_monday_shift_for_october_12():
    assert monday_shifted_holiday(2026, 10, 12) == date(2026, 10, 12)
    assert monday_shifted_holiday(2027, 10, 12) == date(2027, 10, 11)
    assert monday_shifted_holiday(2029, 10, 12) == date(2029, 10, 15)
