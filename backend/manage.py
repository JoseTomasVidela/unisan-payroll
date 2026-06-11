from __future__ import annotations

import argparse
import getpass

from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import (
    Base,
    build_engine,
    is_sqlite_url,
    validate_required_tables,
)
from app.services import create_user, seed_roles_and_permissions


def create_admin(args: argparse.Namespace) -> None:
    settings = get_settings()
    target_engine = build_engine(settings.database_url)

    if is_sqlite_url(settings.database_url):
        Base.metadata.create_all(target_engine)
        with Session(target_engine) as db:
            seed_roles_and_permissions(db)
    else:
        validate_required_tables(target_engine)

    password = args.password or getpass.getpass("Contraseña: ")
    confirmation = args.password or getpass.getpass("Confirmar contraseña: ")
    if password != confirmation:
        raise SystemExit("Las contraseñas no coinciden.")

    with Session(target_engine) as db:
        try:
            user = create_user(
                db,
                username=args.username,
                full_name=args.full_name,
                password=password,
                role_name="ADMIN",
            )
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
    print(f"Administrador creado: {user.username}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Administración de UNISAN Payroll")
    commands = parser.add_subparsers(required=True)

    create = commands.add_parser("create-admin", help="Crear un administrador explícitamente")
    create.add_argument("--username", default="admin")
    create.add_argument("--full-name", default="Administrador")
    create.add_argument("--password", help="Omitir para solicitarla de forma segura")
    create.set_defaults(handler=create_admin)
    return parser


if __name__ == "__main__":
    arguments = build_parser().parse_args()
    arguments.handler(arguments)

