from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import (
    PayrollAuditLog,
    PayrollConcept,
    PayrollConceptRate,
    PayrollCycle,
    User,
)

RATE_SCOPE_SINGLE = "SINGLE_CYCLE"
RATE_SCOPE_FORWARD = "FROM_CYCLE_FORWARD"
VALID_RATE_SCOPES = {RATE_SCOPE_SINGLE, RATE_SCOPE_FORWARD}


@dataclass(frozen=True)
class RateRow:
    concept_id: int
    concept_code: str
    concept_name: str
    cost_center: str
    role_type: str
    contract_type: str | None
    rate_id: int | None
    amount: Decimal | None
    effective_from_cycle_id: int | None
    effective_from_cycle_name: str | None
    effective_to_cycle_id: int | None
    effective_to_cycle_name: str | None
    active: bool


class ConceptRateService:
    def concept(self, db: Session, *, concept_id: int) -> PayrollConcept:
        return self._validate_concept(db, concept_id=concept_id)

    def rate_context(
        self,
        db: Session,
        *,
        rate_id: int,
    ) -> tuple[PayrollConceptRate, PayrollConcept]:
        return self._rate_context(db, rate_id=rate_id)

    def _cycles(self, db: Session) -> dict[int, PayrollCycle]:
        return {cycle.id: cycle for cycle in db.scalars(select(PayrollCycle)).all()}

    def _ordered_active_rates(
        self,
        db: Session,
        *,
        concept_ids: list[int],
        contract_type: str | None = None,
    ) -> list[PayrollConceptRate]:
        if not concept_ids:
            return []
        filters = [
            PayrollConceptRate.concept_id.in_(concept_ids),
            PayrollConceptRate.active.is_(True),
        ]
        if contract_type is None:
            filters.append(PayrollConceptRate.contract_type.is_(None))
        else:
            filters.append(
                (PayrollConceptRate.contract_type == contract_type)
                | PayrollConceptRate.contract_type.is_(None)
            )
        return list(
            db.scalars(
                select(PayrollConceptRate)
                .where(*filters)
                .order_by(
                    PayrollConceptRate.concept_id,
                    PayrollConceptRate.contract_type.is_(None),
                    PayrollConceptRate.id.desc(),
                )
            ).all()
        )

    def _covers_cycle(
        self,
        rate: PayrollConceptRate,
        *,
        target_cycle: PayrollCycle,
        cycles: dict[int, PayrollCycle],
    ) -> bool:
        from_cycle = cycles.get(rate.effective_from_cycle_id)
        to_cycle = cycles.get(rate.effective_to_cycle_id)
        starts_before_target = (
            from_cycle is None or from_cycle.start_date <= target_cycle.start_date
        )
        ends_after_target = (
            to_cycle is None or target_cycle.start_date <= to_cycle.start_date
        )
        return starts_before_target and ends_after_target

    def _overlaps_or_follows_cycle(
        self,
        rate: PayrollConceptRate,
        *,
        target_cycle: PayrollCycle,
        cycles: dict[int, PayrollCycle],
    ) -> bool:
        to_cycle = cycles.get(rate.effective_to_cycle_id)
        if to_cycle is not None and to_cycle.start_date < target_cycle.start_date:
            return False
        from_cycle = cycles.get(rate.effective_from_cycle_id)
        return from_cycle is None or from_cycle.start_date >= target_cycle.start_date or (
            from_cycle.start_date < target_cycle.start_date
            and (to_cycle is None or target_cycle.start_date <= to_cycle.start_date)
        )

    def _previous_cycle(
        self,
        db: Session,
        *,
        target_cycle: PayrollCycle,
    ) -> PayrollCycle | None:
        return db.scalar(
            select(PayrollCycle)
            .where(PayrollCycle.start_date < target_cycle.start_date)
            .order_by(PayrollCycle.start_date.desc())
            .limit(1)
        )

    def _rate_context(
        self,
        db: Session,
        *,
        rate_id: int,
    ) -> tuple[PayrollConceptRate, PayrollConcept]:
        rate = db.get(PayrollConceptRate, rate_id)
        if rate is None:
            raise LookupError("Tarifa no encontrada.")
        concept = db.get(PayrollConcept, rate.concept_id)
        if concept is None:
            raise LookupError("Concepto no encontrado.")
        return rate, concept

    def _validate_concept(
        self,
        db: Session,
        *,
        concept_id: int,
    ) -> PayrollConcept:
        concept = db.get(PayrollConcept, concept_id)
        if concept is None:
            raise LookupError("Concepto no encontrado.")
        return concept

    def _audit(
        self,
        db: Session,
        *,
        user_id: int,
        action_type: str,
        record_id: int,
        old_value: str | None,
        new_value: str | None,
    ) -> None:
        db.add(
            PayrollAuditLog(
                user_id=user_id,
                action_type=action_type,
                table_name="payroll_concept_rates",
                record_id=record_id,
                field_name="amount",
                old_value=old_value,
                new_value=new_value,
            )
        )

    def effective_rates(
        self,
        db: Session,
        *,
        concept_ids: list[int],
        cycle_id: int,
        contract_type: str | None = None,
    ) -> dict[int, PayrollConceptRate]:
        target_cycle = db.get(PayrollCycle, cycle_id)
        if target_cycle is None:
            raise LookupError("Ciclo no encontrado.")
        cycles = self._cycles(db)
        rows = self._ordered_active_rates(
            db,
            concept_ids=concept_ids,
            contract_type=contract_type,
        )
        result: dict[int, PayrollConceptRate] = {}
        for rate in rows:
            if self._covers_cycle(rate, target_cycle=target_cycle, cycles=cycles):
                result.setdefault(rate.concept_id, rate)
        return result

    def list_rates(
        self,
        db: Session,
        *,
        cost_center: str,
        role_type: str,
        cycle_id: int,
        contract_type: str | None = None,
    ) -> list[RateRow]:
        cycle = db.get(PayrollCycle, cycle_id)
        if cycle is None:
            raise LookupError("Ciclo no encontrado.")
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
        cycles = self._cycles(db)
        effective = self.effective_rates(
            db,
            concept_ids=[concept.id for concept in concepts],
            cycle_id=cycle_id,
            contract_type=contract_type,
        )
        rows: list[RateRow] = []
        for concept in concepts:
            rate = effective.get(concept.id)
            from_cycle = cycles.get(rate.effective_from_cycle_id) if rate else None
            to_cycle = cycles.get(rate.effective_to_cycle_id) if rate else None
            rows.append(
                RateRow(
                    concept_id=concept.id,
                    concept_code=concept.concept_code,
                    concept_name=concept.concept_name,
                    cost_center=concept.cost_center,
                    role_type=concept.role_type,
                    contract_type=contract_type if rate is None else rate.contract_type,
                    rate_id=rate.id if rate else None,
                    amount=rate.amount if rate else None,
                    effective_from_cycle_id=rate.effective_from_cycle_id if rate else None,
                    effective_from_cycle_name=from_cycle.cycle_name if from_cycle else None,
                    effective_to_cycle_id=rate.effective_to_cycle_id if rate else None,
                    effective_to_cycle_name=to_cycle.cycle_name if to_cycle else None,
                    active=bool(rate and rate.active),
                )
            )
        return rows

    def _create_rate(
        self,
        db: Session,
        *,
        concept_id: int,
        amount: Decimal,
        contract_type: str | None,
        effective_from_cycle_id: int,
        effective_to_cycle_id: int | None,
        admin: User,
        action_type: str,
        old_value: str | None,
    ) -> PayrollConceptRate:
        now = datetime.utcnow()
        rate = PayrollConceptRate(
            concept_id=concept_id,
            amount=amount,
            contract_type=contract_type,
            effective_from_cycle_id=effective_from_cycle_id,
            effective_to_cycle_id=effective_to_cycle_id,
            created_by=admin.id,
            active=True,
            updated_at=now,
        )
        db.add(rate)
        db.flush()
        self._audit(
            db,
            user_id=admin.id,
            action_type=action_type,
            record_id=rate.id,
            old_value=old_value,
            new_value=str(amount),
        )
        return rate

    def _deactivate_rate(
        self,
        db: Session,
        *,
        rate: PayrollConceptRate,
        admin: User,
        action_type: str,
    ) -> None:
        rate.active = False
        rate.updated_at = datetime.utcnow()
        self._audit(
            db,
            user_id=admin.id,
            action_type=action_type,
            record_id=rate.id,
            old_value=str(rate.amount),
            new_value=None,
        )

    def _close_rate(
        self,
        db: Session,
        *,
        rate: PayrollConceptRate,
        effective_to_cycle_id: int,
        admin: User,
    ) -> None:
        rate.effective_to_cycle_id = effective_to_cycle_id
        rate.updated_at = datetime.utcnow()
        self._audit(
            db,
            user_id=admin.id,
            action_type="RATE_RANGE_CLOSED",
            record_id=rate.id,
            old_value=str(rate.amount),
            new_value=str(rate.amount),
        )

    def save_rate(
        self,
        db: Session,
        *,
        concept_id: int,
        cycle_id: int,
        amount: Decimal,
        apply_mode: str,
        contract_type: str | None,
        admin: User,
    ) -> PayrollConceptRate:
        if apply_mode not in VALID_RATE_SCOPES:
            raise ValueError("Modo de vigencia invalido.")
        if amount < 0:
            raise ValueError("La tarifa no puede ser negativa.")

        target_cycle = db.get(PayrollCycle, cycle_id)
        if target_cycle is None:
            raise LookupError("Ciclo no encontrado.")
        concept = self._validate_concept(db, concept_id=concept_id)
        cycles = self._cycles(db)
        active_rates = list(
            db.scalars(
                select(PayrollConceptRate)
                .where(
                    PayrollConceptRate.concept_id == concept.id,
                    PayrollConceptRate.active.is_(True),
                    PayrollConceptRate.contract_type == contract_type,
                )
                .order_by(PayrollConceptRate.id.desc())
            ).all()
        )
        effective = self.effective_rates(
            db,
            concept_ids=[concept.id],
            cycle_id=cycle_id,
            contract_type=contract_type,
        ).get(concept.id)

        if apply_mode == RATE_SCOPE_SINGLE:
            for rate in active_rates:
                if (
                    rate.effective_from_cycle_id == cycle_id
                    and rate.effective_to_cycle_id == cycle_id
                ):
                    self._deactivate_rate(
                        db,
                        rate=rate,
                        admin=admin,
                        action_type="RATE_SINGLE_CYCLE_REPLACED",
                    )
            old_value = str(effective.amount) if effective else None
            return self._create_rate(
                db,
                concept_id=concept.id,
                amount=amount,
                contract_type=contract_type,
                effective_from_cycle_id=cycle_id,
                effective_to_cycle_id=cycle_id,
                admin=admin,
                action_type="RATE_SINGLE_CYCLE_CREATED",
                old_value=old_value,
            )

        previous_cycle = self._previous_cycle(db, target_cycle=target_cycle)
        for rate in active_rates:
            if not self._overlaps_or_follows_cycle(
                rate,
                target_cycle=target_cycle,
                cycles=cycles,
            ):
                continue
            from_cycle = cycles.get(rate.effective_from_cycle_id)
            if from_cycle is not None and from_cycle.start_date < target_cycle.start_date:
                if previous_cycle is None:
                    self._deactivate_rate(
                        db,
                        rate=rate,
                        admin=admin,
                        action_type="RATE_FORWARD_DEACTIVATED",
                    )
                else:
                    self._close_rate(
                        db,
                        rate=rate,
                        effective_to_cycle_id=previous_cycle.id,
                        admin=admin,
                    )
                continue
            self._deactivate_rate(
                db,
                rate=rate,
                admin=admin,
                action_type="RATE_FORWARD_DEACTIVATED",
            )

        old_value = str(effective.amount) if effective else None
        return self._create_rate(
            db,
            concept_id=concept.id,
            amount=amount,
            contract_type=contract_type,
            effective_from_cycle_id=cycle_id,
            effective_to_cycle_id=None,
            admin=admin,
            action_type="RATE_FORWARD_CREATED",
            old_value=old_value,
        )

    def update_rate(
        self,
        db: Session,
        *,
        rate_id: int,
        cycle_id: int,
        amount: Decimal,
        apply_mode: str,
        contract_type: str | None,
        admin: User,
    ) -> PayrollConceptRate:
        rate, concept = self._rate_context(db, rate_id=rate_id)
        return self.save_rate(
            db,
            concept_id=concept.id,
            cycle_id=cycle_id,
            amount=amount,
            apply_mode=apply_mode,
            contract_type=contract_type if contract_type is not None else rate.contract_type,
            admin=admin,
        )

    def create_versions(
        self,
        db: Session,
        *,
        cycle_id: int,
        cost_center: str,
        role_type: str,
        contract_type: str | None,
        updates: list[tuple[int, Decimal, str]],
        admin: User,
    ) -> None:
        for concept_id, amount, apply_mode in updates:
            concept = self._validate_concept(db, concept_id=concept_id)
            if concept.cost_center != cost_center or concept.role_type != role_type:
                raise ValueError("El concepto no pertenece a la liquidacion seleccionada.")
            self.save_rate(
                db,
                concept_id=concept_id,
                cycle_id=cycle_id,
                amount=amount,
                apply_mode=apply_mode,
                contract_type=contract_type,
                admin=admin,
            )
