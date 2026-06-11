from __future__ import annotations

import unicodedata

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Employee

WORKER_CONTRACTS = [
    ("Cristian Gonzalez", "OLD"),
    ("Rodrigo Bascunan", "NEW"),
    ("Luis Dugo", "OLD"),
    ("Alfredo Cona", "NEW"),
    ("Cesar Moreno", "OLD"),
    ("Daniel Diaz", "NEW"),
    ("Fernando Diaz", "NEW"),
    ("Luis Acevedo", "NEW"),
    ("Maximiliano Arancibia", "OLD"),
    ("Patricio Cubillos", "OLD"),
    ("Pedro Arcos", "NEW"),
    ("Roberto Briones", "NEW"),
    ("Roberto Ramirez", "OLD"),
    ("Alexander Marchant", "OLD"),
    ("Boris Lopez", "OLD"),
    ("Edgar Benavides", "NEW"),
    ("Byron Lopez", "NEW"),
    ("Juan Santibanez", "OLD"),
    ("Gerald Aguayo", "NEW"),
    ("Jose Oca", "OLD"),
    ("Victor Araneda", "OLD"),
    ("Osman Perez", "NEW"),
    ("Alejandro Osorio", "OLD"),
    ("Luis Cubillos", "NEW"),
    ("Gilmar Ospino", "NEW"),
    ("Nelson Paredes", "NEW"),
    ("Carlos Correa", "NEW"),
    ("Juan Aravena", "OLD"),
    ("Daniel Escobar", "NEW"),
    ("Jordan Gaete", "NEW"),
    ("Cristian Araya", "OLD"),
    ("Gonzalo Gonzalez", "OLD"),
    ("Juan Cuadra", "OLD"),
]


def normalize_name(value: str) -> str:
    no_marks = "".join(
        char
        for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )
    return " ".join(no_marks.strip().lower().split())


def sync_worker_contracts() -> None:
    with SessionLocal() as db:
        employees = list(db.scalars(select(Employee).order_by(Employee.id)).all())
        by_normalized_name: dict[str, list[Employee]] = {}
        for employee in employees:
            by_normalized_name.setdefault(
                normalize_name(employee.employee_name),
                [],
            ).append(employee)

        created = 0
        updated = 0
        for worker_name, contract_type in WORKER_CONTRACTS:
            normalized_name = normalize_name(worker_name)
            matches = by_normalized_name.get(normalized_name, [])
            if matches:
                for employee in matches:
                    if employee.contract_type != contract_type:
                        employee.contract_type = contract_type
                        updated += 1
                continue

            employee = Employee(
                employee_name=worker_name,
                role_type="UNASSIGNED",
                contract_type=contract_type,
            )
            db.add(employee)
            db.flush()
            by_normalized_name.setdefault(normalized_name, []).append(employee)
            created += 1

        db.commit()
        print(
            f"Sincronizacion completada. Trabajadores creados: {created}. "
            f"Registros actualizados: {updated}."
        )


if __name__ == "__main__":
    sync_worker_contracts()
