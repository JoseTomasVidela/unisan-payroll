from __future__ import annotations

import csv
from pathlib import Path

from app.concept_rate_source import extract_rate_occurrences, rate_options
from seed_payroll_concepts import SEED_ITEMS, SOURCE_FILE, verify_source

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "docs"
CSV_OUTPUT = OUTPUT_DIR / "payroll_07_rate_alternatives_report.csv"
MD_OUTPUT = OUTPUT_DIR / "payroll_07_rate_alternatives_report.md"


def source_text(items) -> str:
    return "; ".join(f"{item.sheet_name}!{item.cell}" for item in items)


def main() -> None:
    verify_source()
    occurrences = extract_rate_occurrences(SOURCE_FILE, SEED_ITEMS)
    rows = []
    conflict_count = 0
    for seed in SEED_ITEMS:
        key = (seed.source_type, seed.role_type, seed.concept_code)
        options = rate_options(occurrences.get(key, []))
        status = "OK" if len(options) == 1 and seed.amount in options else "CONFLICTO"
        if status == "CONFLICTO":
            conflict_count += 1
        proposed_sources = source_text(options.get(seed.amount, []))
        alternatives = [
            f"{amount}: {source_text(items)}"
            for amount, items in sorted(options.items())
            if amount != seed.amount
        ]
        rows.append(
            {
                "status": status,
                "concept_code": seed.concept_code,
                "concept_name": seed.concept_name,
                "cost_center": seed.cost_center,
                "role_type": seed.role_type,
                "proposed_rate": f"{seed.amount:.4f}",
                "proposed_source_cells": proposed_sources,
                "other_rates_and_source_cells": " | ".join(alternatives),
                "all_rates_found": ", ".join(f"{amount:.4f}" for amount in sorted(options)),
                "occurrence_count": sum(len(items) for items in options.values()),
                "sheet_names": ", ".join(sorted({item.sheet_name for items in options.values() for item in items})),
            }
        )

    with CSV_OUTPUT.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Reporte de tarifas alternativas - PRODUCCION D&R 2.xlsx",
        "",
        "Estado: revisión manual requerida. No se insertaron datos.",
        "",
        f"- Conceptos analizados: {len(rows)}",
        f"- Conceptos con CONFLICTO: {conflict_count}",
        f"- Conceptos sin conflicto: {len(rows) - conflict_count}",
        "- Hoja fuente detectada: `May-26`",
        "- Tarifa leída desde la columna `C` de cada ocurrencia.",
        "",
        "| Estado | Centro | Rol | Concepto | Tarifa propuesta | Otras tarifas encontradas | Origen propuesta |",
        "|---|---|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['status']} | {row['cost_center']} | {row['role_type']} | "
            f"{row['concept_name']} | {row['proposed_rate']} | "
            f"{row['other_rates_and_source_cells'] or '-'} | "
            f"{row['proposed_source_cells'] or '-'} |"
        )
    lines.extend(
        [
            "",
            "El CSV asociado contiene las celdas de origen completas para cada tarifa.",
            "Los conceptos marcados `CONFLICTO` quedan excluidos por el script de seed.",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Reporte generado: {MD_OUTPUT}")
    print(f"Detalle CSV generado: {CSV_OUTPUT}")
    print(f"CONFLICTO={conflict_count} OK={len(rows) - conflict_count}")


if __name__ == "__main__":
    main()
