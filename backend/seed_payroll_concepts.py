from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.concept_rate_source import extract_rate_occurrences, rate_options
from app.database import build_engine, is_sqlite_url
from app.models import PayrollConcept, PayrollConceptRate

SOURCE_FILE = Path(__file__).resolve().parents[1] / "ref" / "PRODUCCION D&R 2.xlsx"
SOURCE_SHA256 = "0EB9878074D080515ED70CDACE2BCA3FD757EEACDAE7974F42023FDD05AFEE01"


@dataclass(frozen=True)
class SeedItem:
    concept_code: str
    concept_name: str
    db_field: str
    source_type: str
    cost_center: str
    role_type: str
    display_order: int
    amount: Decimal


def item(
    concept_code: str,
    concept_name: str,
    db_field: str,
    source_type: str,
    role_type: str,
    display_order: int,
    amount: str,
) -> SeedItem:
    return SeedItem(
        concept_code=concept_code,
        concept_name=concept_name,
        db_field=db_field,
        source_type=source_type,
        cost_center=source_type,
        role_type=role_type,
        display_order=display_order,
        amount=Decimal(amount),
    )


DRIVER_DR = [
    item("DISPATCH_RETRIEVAL", "Despacho / Retiro", "dispatch_flag", "DR", "DRIVER", 1, "751.4100"),
    item("ENTRY_BEFORE_1930", "Entrada < 19:30", "entry_before_1930_qty", "DR", "DRIVER", 2, "2506.3674"),
    item("EXIT_AFTER_1930", "Salida > 19:30", "exit_after_1930_qty", "DR", "DRIVER", 3, "8772.2858"),
    item("FAIR_WEEK_1", "Feria Semana 01", "fair_week_1_flag", "DR", "DRIVER", 4, "10025.4695"),
    item("FAIR_WEEK_2", "Feria Semana 02", "fair_week_2_flag", "DR", "DRIVER", 5, "12531.8369"),
    item("OUTSIDE_RADIUS", "Fuera Radio Normal", "outside_radius_flag", "DR", "DRIVER", 6, "3759.5511"),
    item("OUTSIDE_RADIUS_V_REGION", "Fuera Radio V Región", "outside_radius_v_region_qty", "DR", "DRIVER", 7, "6265.9184"),
    item("SATURDAY_WEEK_1", "Sabado Semana 01", "saturday_week_1_qty", "DR", "DRIVER", 8, "20050.9390"),
    item("SUNDAY_WEEK_1", "Domingo Semana 01", "sunday_week_1_qty", "DR", "DRIVER", 9, "25063.6738"),
    item("CLIENT_TRIPS", "Viajes Por Cliente", "client_trips_qty", "DR", "DRIVER", 10, "6265.9184"),
    item("SATURDAY_AFTER_1600", "Sábado > 16:00", "saturday_after_1600_qty", "DR", "DRIVER", 11, "10025.4695"),
    item("SUNDAY_AFTER_1600", "Domingo > 16:00", "sunday_after_1600_qty", "DR", "DRIVER", 12, "11278.6532"),
    item("SATURDAY_WEEK_2", "Sabado Semana 02", "saturday_week_2_qty", "DR", "DRIVER", 13, "23810.4901"),
    item("SUNDAY_WEEK_2", "Domingo Semana 02", "sunday_week_2_qty", "DR", "DRIVER", 14, "28823.2249"),
    item("WEEKEND_DRYING", "Secado Fin de Semana", "weekend_drying_qty", "DR", "DRIVER", 15, "550.9788"),
    item("EVENT", "Evento", "event_flag", "DR", "DRIVER", 16, "751.4413"),
    item("WATER_POINT", "Punto de Agua", "water_point_flag", "DR", "DRIVER", 17, "1492.1098"),
    item("LARGE_TRASH_BIN", "Basurero Grande", "large_trash_bin_qty", "DR", "DRIVER", 18, "1056.7350"),
    item("SMALL_TRASH_BIN", "Basurero chico", "small_trash_bin_qty", "DR", "DRIVER", 19, "263.9250"),
    item("FOSA", "Fosa", "fosa_qty", "DR", "DRIVER", 20, "1492.4700"),
]

ASSISTANT_DR = [
    item("DISPATCH_RETRIEVAL", "Despacho / Retiro", "dispatch_flag", "DR", "ASSISTANT", 1, "376.3068"),
    item("ENTRY_BEFORE_1930", "Entrada < 19:30", "entry_before_1930_qty", "DR", "ASSISTANT", 2, "1253.1837"),
    item("EXIT_AFTER_1930", "Salida > 19:30", "exit_after_1930_qty", "DR", "ASSISTANT", 3, "7519.1021"),
    item("FAIR_WEEK_1", "Feria Semana 01", "fair_week_1_flag", "DR", "ASSISTANT", 4, "7519.1021"),
    item("FAIR_WEEK_2", "Feria Semana 02", "fair_week_2_flag", "DR", "ASSISTANT", 5, "10652.6475"),
    item("OUTSIDE_RADIUS", "Fuera Radio Normal", "outside_radius_flag", "DR", "ASSISTANT", 6, "2819.3702"),
    item("OUTSIDE_RADIUS_V_REGION", "Fuera Radio V Región", "outside_radius_v_region_qty", "DR", "ASSISTANT", 7, "5012.7348"),
    item("SATURDAY_WEEK_1", "Sabado Semana 01", "saturday_week_1_qty", "DR", "ASSISTANT", 8, "15038.2043"),
    item("SUNDAY_WEEK_1", "Domingo Semana 01", "sunday_week_1_qty", "DR", "ASSISTANT", 9, "20050.9390"),
    item("CLIENT_TRIPS", "Viajes Por Cliente", "client_trips_qty", "DR", "ASSISTANT", 10, "5012.7348"),
    item("SATURDAY_AFTER_1600", "Sábado > 16:00", "saturday_after_1600_qty", "DR", "ASSISTANT", 11, "8772.2858"),
    item("SUNDAY_AFTER_1600", "Domingo > 16:00", "sunday_after_1600_qty", "DR", "ASSISTANT", 12, "10025.4695"),
    item("SATURDAY_WEEK_2", "Sabado Semana 02", "saturday_week_2_qty", "DR", "ASSISTANT", 13, "18797.7553"),
    item("SUNDAY_WEEK_2", "Domingo Semana 02", "sunday_week_2_qty", "DR", "ASSISTANT", 14, "23810.4901"),
    item("WEEKEND_DRYING", "Secado Fin de Semana", "weekend_drying_qty", "DR", "ASSISTANT", 15, "275.3100"),
    item("EVENT", "Evento", "event_flag", "DR", "ASSISTANT", 16, "376.7400"),
    item("WATER_POINT", "Punto de Agua", "water_point_flag", "DR", "ASSISTANT", 17, "728.6400"),
    item("LARGE_TRASH_BIN", "Basurero Grande", "large_trash_bin_qty", "DR", "ASSISTANT", 18, "951.1650"),
    item("SMALL_TRASH_BIN", "Basurero chico", "small_trash_bin_qty", "DR", "ASSISTANT", 19, "238.0500"),
    item("FOSA", "Fosa", "fosa_qty", "DR", "ASSISTANT", 20, "1458.3150"),
]

DRIVER_SERVICES = [
    item("CLEANING", "Aseo", "cleaning_flag", "SERVICES", "DRIVER", 1, "313.2959"),
    item("DRYING", "Secado", "drying_flag", "SERVICES", "DRIVER", 2, "275.7004"),
    item("DISPATCH_RETRIEVAL", "Despacho / Retiro", "dispatch_flag", "SERVICES", "DRIVER", 3, "751.9102"),
    item("ENTRY_BEFORE_0730", "Entrada < 07:30", "entry_before_0730_qty", "SERVICES", "DRIVER", 4, "2506.3674"),
    item("EXIT_AFTER_1930", "Salida > 19:30", "exit_after_1930_qty", "SERVICES", "DRIVER", 5, "8772.2858"),
    item("OUTSIDE_RADIUS", "Fuera Radio Normal", "outside_radius_flag", "SERVICES", "DRIVER", 6, "3759.5511"),
    item("OUTSIDE_RADIUS_V_REGION", "Fuera Radio V Región", "outside_radius_v_region_qty", "SERVICES", "DRIVER", 7, "6265.9184"),
    item("KIT_DELIVERY", "Entrega Kit", "kit_delivery_flag", "SERVICES", "DRIVER", 8, "313.2959"),
    item("LAVATORY_LOAD", "Carga Lavamanos", "lavatory_load_flag", "SERVICES", "DRIVER", 9, "31.3296"),
    item("SATURDAY_WEEK_1", "Sabado", "saturday_week_1_qty", "SERVICES", "DRIVER", 10, "11905.2450"),
    item("SUNDAY_WEEK_1", "Domingo", "sunday_week_1_qty", "SERVICES", "DRIVER", 11, "15038.2043"),
    item("WEEKEND_CLEANING", "Aseo Fin de Semana", "weekend_cleaning_qty", "SERVICES", "DRIVER", 12, "17.4319"),
    item("WEEKEND_DRYING", "Secado Fin de Semana", "weekend_drying_qty", "SERVICES", "DRIVER", 13, "551.4008"),
    item("SATURDAY_AFTER_1600", "Sabado > 16:00", "saturday_after_1600_qty", "SERVICES", "DRIVER", 14, "10025.4695"),
    item("SUNDAY_AFTER_1600", "Domingo > 16:00", "sunday_after_1600_qty", "SERVICES", "DRIVER", 15, "11278.6532"),
    item("SATURDAY_WEEK_2", "Sabado Semana 02", "saturday_week_2_qty", "SERVICES", "DRIVER", 16, "11905.2450"),
    item("SUNDAY_WEEK_2", "Domingo Semana 02", "sunday_week_2_qty", "SERVICES", "DRIVER", 17, "15038.2043"),
    item("RILES_SUCTION", "Succión Riles (M3)", "riles_suction_flag", "SERVICES", "DRIVER", 18, "2527.4700"),
]

ASSISTANT_SERVICES = [
    item("CLEANING", "Aseo", "cleaning_flag", "SERVICES", "ASSISTANT", 1, "138.6900"),
    item("DRYING", "Secado", "drying_flag", "SERVICES", "ASSISTANT", 2, "138.6900"),
    item("DISPATCH_RETRIEVAL", "Despacho / Retiro", "dispatch_flag", "SERVICES", "ASSISTANT", 3, "376.7400"),
    item("ENTRY_BEFORE_0730", "Entrada < 07:30", "entry_before_0730_qty", "SERVICES", "ASSISTANT", 4, "1253.3850"),
    item("EXIT_AFTER_1930", "Salida > 19:30", "exit_after_1930_qty", "SERVICES", "ASSISTANT", 5, "7519.2750"),
    item("OUTSIDE_RADIUS", "Fuera Radio Normal", "outside_radius_flag", "SERVICES", "ASSISTANT", 6, "2820.3750"),
    item("OUTSIDE_RADIUS_V_REGION", "Fuera Radio V Región", "outside_radius_v_region_qty", "SERVICES", "ASSISTANT", 7, "5012.5050"),
    item("KIT_DELIVERY", "Entrega Kit", "kit_delivery_flag", "SERVICES", "ASSISTANT", 8, "138.6900"),
    item("LAVATORY_LOAD", "Carga Lavamanos", "lavatory_load_flag", "SERVICES", "ASSISTANT", 9, "24.8400"),
    item("SATURDAY_WEEK_1", "Sabado", "saturday_week_1_qty", "SERVICES", "ASSISTANT", 10, "11905.6050"),
    item("SUNDAY_WEEK_1", "Domingo", "sunday_week_1_qty", "SERVICES", "ASSISTANT", 11, "15038.5500"),
    item("WEEKEND_CLEANING", "Aseo Fin de Semana", "weekend_cleaning_qty", "SERVICES", "ASSISTANT", 12, "275.3100"),
    item("WEEKEND_DRYING", "Secado Fin de Semana", "weekend_drying_qty", "SERVICES", "ASSISTANT", 13, "275.3100"),
    item("SATURDAY_AFTER_1600", "Sabado > 16:00", "saturday_after_1600_qty", "SERVICES", "ASSISTANT", 14, "8772.6600"),
    item("SUNDAY_AFTER_1600", "Domingo > 16:00", "sunday_after_1600_qty", "SERVICES", "ASSISTANT", 15, "10025.0100"),
    item("SATURDAY_WEEK_2", "Sabado Semana 02", "saturday_week_2_qty", "SERVICES", "ASSISTANT", 16, "11905.6050"),
    item("SUNDAY_WEEK_2", "Domingo Semana 02", "sunday_week_2_qty", "SERVICES", "ASSISTANT", 17, "15038.5500"),
    item("RILES_SUCTION", "Succión Riles (M3)", "riles_suction_flag", "SERVICES", "ASSISTANT", 18, "1253.3850"),
]

SEED_ITEMS = DRIVER_DR + ASSISTANT_DR + DRIVER_SERVICES + ASSISTANT_SERVICES


def classify_seed_items() -> tuple[list[SeedItem], list[SeedItem]]:
    occurrences = extract_rate_occurrences(SOURCE_FILE, SEED_ITEMS)
    approved: list[SeedItem] = []
    conflicts: list[SeedItem] = []
    for seed in SEED_ITEMS:
        key = (seed.source_type, seed.role_type, seed.concept_code)
        options = rate_options(occurrences.get(key, []))
        if len(options) == 1 and seed.amount in options:
            approved.append(seed)
        else:
            conflicts.append(seed)
    return approved, conflicts


def verify_source() -> None:
    digest = hashlib.sha256(SOURCE_FILE.read_bytes()).hexdigest().upper()
    if digest != SOURCE_SHA256:
        raise SystemExit("La planilla fuente cambió. Revise nuevamente la propuesta antes de aplicar.")


def validate_schema(target_engine) -> None:
    schema = inspect(target_engine)
    tables = set(schema.get_table_names())
    required = {"payroll_concepts", "payroll_concept_rates"}
    if missing := sorted(required - tables):
        raise SystemExit("Faltan tablas requeridas: " + ", ".join(missing))
    concept_columns = {column["name"] for column in schema.get_columns("payroll_concepts")}
    required_columns = {
        "concept_code",
        "concept_name",
        "db_field",
        "source_type",
        "cost_center",
        "role_type",
        "display_order",
        "active",
    }
    if missing := sorted(required_columns - concept_columns):
        raise SystemExit("Faltan columnas en payroll_concepts: " + ", ".join(missing))


def print_proposal() -> None:
    approved, conflicts = classify_seed_items()
    print("Modo vista previa. No se insertarán datos.")
    print(f"Fuente: {SOURCE_FILE}")
    print(f"SHA256: {SOURCE_SHA256}")
    print(f"Conceptos sin conflicto: {len(approved)}")
    print(f"Conceptos excluidos por conflicto: {len(conflicts)}")
    for seed in SEED_ITEMS:
        status = "APROBABLE" if seed in approved else "CONFLICTO"
        print(
            f"{status:10} {seed.source_type:8} {seed.role_type:9} {seed.display_order:02} "
            f"{seed.concept_code:24} {seed.amount:>12} {seed.concept_name}"
        )


def apply_seed(db: Session) -> None:
    approved, conflicts = classify_seed_items()
    if conflicts:
        print(f"Se excluirán {len(conflicts)} conceptos marcados CONFLICTO.")
    for seed in approved:
        concepts = list(
            db.scalars(
                select(PayrollConcept).where(
                    PayrollConcept.concept_code == seed.concept_code,
                    PayrollConcept.source_type == seed.source_type,
                    PayrollConcept.cost_center == seed.cost_center,
                    PayrollConcept.role_type == seed.role_type,
                )
            ).all()
        )
        if len(concepts) > 1:
            raise ValueError(f"Concepto duplicado existente: {seed}")
        concept = concepts[0] if concepts else PayrollConcept()
        if not concepts:
            db.add(concept)
        concept.concept_code = seed.concept_code
        concept.concept_name = seed.concept_name
        concept.db_field = seed.db_field
        concept.source_type = seed.source_type
        concept.cost_center = seed.cost_center
        concept.role_type = seed.role_type
        concept.display_order = seed.display_order
        concept.active = True
        db.flush()

        rates = list(
            db.scalars(
                select(PayrollConceptRate).where(
                    PayrollConceptRate.concept_id == concept.id,
                    PayrollConceptRate.active.is_(True),
                )
            ).all()
        )
        if len(rates) > 1:
            raise ValueError(f"Más de una tarifa activa para {seed}")
        rate = rates[0] if rates else PayrollConceptRate(concept_id=concept.id, active=True)
        if not rates:
            db.add(rate)
        rate.amount = seed.amount
    db.commit()


def apply_base_concepts(db: Session) -> None:
    for seed in SEED_ITEMS:
        concepts = list(
            db.scalars(
                select(PayrollConcept).where(
                    PayrollConcept.concept_code == seed.concept_code,
                    PayrollConcept.source_type == seed.source_type,
                    PayrollConcept.cost_center == seed.cost_center,
                    PayrollConcept.role_type == seed.role_type,
                )
            ).all()
        )
        if len(concepts) > 1:
            raise ValueError(f"Concepto duplicado existente: {seed}")
        concept = concepts[0] if concepts else PayrollConcept()
        if not concepts:
            db.add(concept)
        concept.concept_code = seed.concept_code
        concept.concept_name = seed.concept_name
        concept.db_field = seed.db_field
        concept.source_type = seed.source_type
        concept.cost_center = seed.cost_center
        concept.role_type = seed.role_type
        concept.display_order = seed.display_order
        concept.active = True
    db.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed controlado de conceptos y tarifas")
    parser.add_argument("--apply", action="store_true", help="Aplicar el seed en SQLite local")
    parser.add_argument(
        "--apply-concepts-only",
        action="store_true",
        help="Crear o actualizar conceptos base sin insertar tarifas",
    )
    args = parser.parse_args()
    verify_source()
    print_proposal()
    if not args.apply and not args.apply_concepts_only:
        return
    if args.apply and args.apply_concepts_only:
        raise SystemExit("Seleccione solo un modo de aplicacion.")

    settings = get_settings()
    if not is_sqlite_url(settings.database_url):
        raise SystemExit("Este seed está bloqueado para MySQL/Azure.")
    target_engine = build_engine(settings.database_url)
    validate_schema(target_engine)
    with Session(target_engine) as db:
        try:
            if args.apply_concepts_only:
                apply_base_concepts(db)
            else:
                apply_seed(db)
        except Exception:
            db.rollback()
            raise
    if args.apply_concepts_only:
        print("Conceptos base aplicados sin tarifas en SQLite local.")
    else:
        print("Seed aplicado correctamente en SQLite local.")


if __name__ == "__main__":
    main()
