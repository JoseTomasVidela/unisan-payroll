from __future__ import annotations

import json
import smtplib
from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, inspect, select, text
from sqlalchemy.orm import Session

from .config import Settings, get_settings
from .database import (
    Base,
    check_connection,
    engine,
    get_db,
    is_sqlite_url,
    validate_database_url,
    validate_required_tables,
)
from .dependencies import get_current_user, require_permission
from .employee_names import (
    names_refer_to_same_person,
    normalize_employee_name,
    parse_personnel_name,
)
from .emailer import send_settlement_email, send_test_email
from .exporter import export_csv_bytes, export_file_name, export_pdf_bytes, export_xlsx_bytes
from .holidays import ALLOWED_HOLIDAY_SCOPES, HolidayService
from .importer import ensure_workbook_cycles, find_possible_reimports, parse_workbook, persist_import
from .models import (
    Employee,
    PayrollAuditLog,
    PayrollCycle,
    PayrollExportLog,
    PayrollHoliday,
    PayrollImport,
    PayrollManualAdjustment,
    PayrollRecord,
    PayrollCellOverride,
    Permission,
    Role,
    User,
)
from .rates import ConceptRateService
from .schemas import (
    CycleResponse,
    EmployeeOptionResponse,
    HolidayCreateRequest,
    HolidayResponse,
    HolidayUpdateRequest,
    ImportHistoryResponse,
    ImportResponse,
    LoginRequest,
    LoginResponse,
    ManualAdjustmentCreateRequest,
    ManualAdjustmentResponse,
    ManualAdjustmentUpdateRequest,
    ManualAdjustmentAuditResponse,
    PermissionResponse,
    RateCreateRequest,
    RateListItemResponse,
    RateUpdateRequest,
    RoleResponse,
    SearchEmployeeOptionResponse,
    SearchResponse,
    SettlementCellUpdateRequest,
    SettlementEmailRequest,
    SettlementResponse,
    SettlementRateUpdateRequest,
    WorkerCreateRequest,
    WorkerListItemResponse,
    WorkerUpdateRequest,
    UserActiveUpdate,
    UserCreate,
    UserResponse,
)
from .security import create_access_token
from .settlements import SettlementEngine
from .services import (
    authenticate,
    create_user,
    seed_roles_and_permissions,
    serialize_user,
)
from seed_payroll_concepts import apply_base_concepts


def bootstrap(
    settings: Settings | None = None,
    target_engine=engine,
) -> None:
    settings = settings or get_settings()
    validate_database_url(settings.database_url)

    if not is_sqlite_url(settings.database_url):
        validate_required_tables(target_engine)
        return

    Base.metadata.create_all(target_engine)
    ensure_local_sqlite_extensions(target_engine)
    with Session(target_engine) as db:
        seed_roles_and_permissions(db)
        apply_base_concepts(db)
        if settings.bootstrap_admin_username and settings.bootstrap_admin_password:
            existing = db.scalar(
                select(User).where(
                    User.username == settings.bootstrap_admin_username.strip().lower()
                )
            )
            if existing is None:
                create_user(
                    db,
                    username=settings.bootstrap_admin_username,
                    full_name=settings.bootstrap_admin_name,
                    password=settings.bootstrap_admin_password,
                    role_name="ADMIN",
                )


def ensure_local_sqlite_extensions(target_engine) -> None:
    inspector = inspect(target_engine)
    employee_columns = {
        column["name"] for column in inspector.get_columns("payroll_employees")
    }
    rate_columns = {
        column["name"] for column in inspector.get_columns("payroll_concept_rates")
    }
    adjustment_columns = {
        column["name"] for column in inspector.get_columns("payroll_manual_adjustments")
    }
    statements: list[str] = []
    if "contract_type" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN contract_type VARCHAR(16) NULL"
        )
    if "rut" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN rut VARCHAR(32) NULL"
        )
    if "email" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN email VARCHAR(255) NULL"
        )
    if "cargo" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN cargo VARCHAR(180) NULL"
        )
    if "first_name" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN first_name VARCHAR(80) NULL"
        )
    if "middle_name" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN middle_name VARCHAR(80) NULL"
        )
    if "paternal_surname" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN paternal_surname VARCHAR(80) NULL"
        )
    if "maternal_surname" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN maternal_surname VARCHAR(80) NULL"
        )
    if "contract_type" not in rate_columns:
        statements.append(
            "ALTER TABLE payroll_concept_rates ADD COLUMN contract_type VARCHAR(16) NULL"
        )
    if "active" not in adjustment_columns:
        statements.append(
            "ALTER TABLE payroll_manual_adjustments ADD COLUMN active BOOLEAN NOT NULL DEFAULT 1"
        )
    if "created_by" not in adjustment_columns:
        statements.append(
            "ALTER TABLE payroll_manual_adjustments ADD COLUMN created_by INTEGER NULL"
        )
    if "updated_by" not in adjustment_columns:
        statements.append(
            "ALTER TABLE payroll_manual_adjustments ADD COLUMN updated_by INTEGER NULL"
        )
    if "created_at" not in adjustment_columns:
        statements.append(
            "ALTER TABLE payroll_manual_adjustments ADD COLUMN created_at DATETIME NULL"
        )
    if "updated_at" not in adjustment_columns:
        statements.append(
            "ALTER TABLE payroll_manual_adjustments ADD COLUMN updated_at DATETIME NULL"
        )
    if "deleted_at" not in adjustment_columns:
        statements.append(
            "ALTER TABLE payroll_manual_adjustments ADD COLUMN deleted_at DATETIME NULL"
        )
    if not statements:
        return
    with target_engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
        connection.execute(
            text(
                "UPDATE payroll_manual_adjustments "
                "SET active = COALESCE(active, 1), created_at = COALESCE(created_at, CURRENT_TIMESTAMP)"
            )
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    bootstrap()
    yield


app = FastAPI(title="UNISAN Payroll API", version="1.0.0", lifespan=lifespan)
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)
settlement_engine = SettlementEngine()
concept_rate_service = ConceptRateService()
holiday_service = HolidayService()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_BUILD_DIR = PROJECT_ROOT / "frontend" / "build"
FRONTEND_ASSETS_DIR = FRONTEND_BUILD_DIR / "assets"


def normalize_contract_type(contract_type: str | None) -> str | None:
    if contract_type is None:
        return None
    normalized = contract_type.strip().upper()
    if not normalized:
        return None
    if normalized not in {"NEW", "OLD"}:
        raise HTTPException(status_code=400, detail="Contrato invalido.")
    return normalized


def normalize_rut(rut: str | None) -> str | None:
    if rut is None:
        return None
    normalized = rut.strip().upper()
    return normalized or None


def normalize_email(email: str | None) -> str | None:
    if email is None:
        return None
    normalized = email.strip().lower()
    return normalized or None


def normalize_cargo(cargo: str | None) -> str | None:
    if cargo is None:
        return None
    normalized = " ".join(cargo.strip().split())
    return normalized or None


def apply_employee_name_parts(employee: Employee, employee_name: str) -> None:
    parsed = parse_personnel_name(employee_name)
    employee.first_name = parsed.given_names[0] if len(parsed.given_names) >= 1 else None
    employee.middle_name = parsed.given_names[1] if len(parsed.given_names) >= 2 else None
    employee.paternal_surname = parsed.paternal_surname or None
    employee.maternal_surname = parsed.maternal_surname or None


def employee_display_name(employee: Employee) -> str:
    parts = [
        employee.first_name,
        employee.middle_name,
        employee.paternal_surname,
        employee.maternal_surname,
    ]
    full_name = " ".join(part.strip() for part in parts if part and part.strip())
    return full_name or employee.employee_name


def grouped_employee_display_name(matches: list[Employee]) -> str:
    for employee in matches:
        full_name = employee_display_name(employee)
        if full_name and full_name != employee.employee_name:
            return full_name
    worker = min(matches, key=lambda item: item.id)
    return employee_display_name(worker)


def find_related_employees_by_name(db: Session, employee_name: str) -> list[Employee]:
    normalized_target = normalize_employee_name(employee_name)
    if not normalized_target:
        return []
    employees = list(db.scalars(select(Employee).order_by(Employee.id)).all())
    return [
        employee
        for employee in employees
        if names_refer_to_same_person(employee.employee_name, employee_name)
    ]


def normalize_holiday_scope(holiday_scope: str) -> str:
    normalized = holiday_scope.strip().upper()
    if normalized not in ALLOWED_HOLIDAY_SCOPES:
        raise HTTPException(status_code=400, detail="Tipo de feriado invalido.")
    return normalized


def normalize_adjustment_type(adjustment_type: str) -> str:
    normalized = adjustment_type.strip().upper()
    allowed = {"VACATION", "BONUS", "MANUAL_ADJUSTMENT"}
    if normalized not in allowed:
        raise HTTPException(status_code=400, detail="Tipo de ajuste invalido.")
    return normalized


def normalize_adjustment_description(description: str | None) -> str | None:
    if description is None:
        return None
    normalized = " ".join(description.strip().split())
    return normalized or None


def effective_adjustment_name(adjustment_type: str, description: str | None) -> str:
    normalized = normalize_adjustment_description(description)
    if normalized:
        return normalized
    defaults = {
        "VACATION": "Vacaciones",
        "BONUS": "Bono",
        "MANUAL_ADJUSTMENT": "Ajuste manual",
    }
    return defaults[normalize_adjustment_type(adjustment_type)]


def _serialize_adjustment(adjustment: PayrollManualAdjustment, history_rows) -> ManualAdjustmentResponse:
    return ManualAdjustmentResponse(
        id=adjustment.id,
        cycle_id=adjustment.cycle_id,
        employee_id=adjustment.employee_id,
        cost_center=adjustment.cost_center,
        role_type=adjustment.role_type,
        adjustment_type=adjustment.adjustment_type,
        description=adjustment.adjustment_name,
        units=adjustment.units,
        amount=adjustment.amount,
        observations=adjustment.notes,
        active=adjustment.active,
        created_at=adjustment.created_at,
        updated_at=adjustment.updated_at,
        deleted_at=adjustment.deleted_at,
        history=[
            ManualAdjustmentAuditResponse(
                id=audit.id,
                action_type=audit.action_type,
                old_value=audit.old_value,
                new_value=audit.new_value,
                action_date=audit.action_date,
                user_name=username,
            )
            for audit, username in history_rows
        ],
    )


def _history_rows_for_adjustments(db: Session, adjustment_ids: list[int]) -> dict[int, list[tuple[PayrollAuditLog, str | None]]]:
    if not adjustment_ids:
        return {}
    rows = db.execute(
        select(PayrollAuditLog, User.username)
        .outerjoin(User, User.id == PayrollAuditLog.user_id)
        .where(PayrollAuditLog.table_name == "payroll_manual_adjustments")
        .where(PayrollAuditLog.record_id.in_(adjustment_ids))
        .order_by(PayrollAuditLog.action_date.desc(), PayrollAuditLog.id.desc())
    ).all()
    grouped: dict[int, list[tuple[PayrollAuditLog, str | None]]] = {}
    for audit, username in rows:
        grouped.setdefault(audit.record_id, []).append((audit, username))
    return grouped


def _serialize_holiday(holiday: PayrollHoliday) -> HolidayResponse:
    return HolidayResponse(
        id=holiday.id if holiday.id else None,
        holiday_date=holiday.holiday_date,
        holiday_name=holiday.holiday_name,
        holiday_scope=holiday.holiday_scope,
        active=holiday.active,
        is_default=holiday.is_default,
        editable=bool(holiday.id),
    )


def normalize_cost_center(cost_center: str | None) -> str | None:
    if cost_center is None:
        return None
    normalized = cost_center.strip().upper()
    if not normalized:
        return None
    if normalized not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Centro de costo invalido.")
    return normalized


def normalize_role_type(role_type: str | None) -> str | None:
    if role_type is None:
        return None
    normalized = role_type.strip().upper()
    if not normalized:
        return None
    if normalized not in {"DRIVER", "ASSISTANT"}:
        raise HTTPException(status_code=400, detail="Cargo invalido.")
    return normalized


def _to_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value))


def _serialize_settlement_payload(payload: dict[str, object]) -> dict[str, object]:
    return {
        "employee": payload["employee"],
        "cycle": payload["cycle"],
        "cost_center": payload["cost_center"],
        "role_type": payload["role_type"],
        "dates": payload["dates"],
        "statuses": payload["statuses"],
        "rows": [
            {
                "row_type": row["row_type"],
                "concept_id": row["concept_id"],
                "rate_id": row["rate_id"],
                "concept_code": row["concept_code"],
                "concept_name": row["concept_name"],
                "db_field": row["db_field"],
                "units": _to_decimal(row["units"]),
                "rate": _to_decimal(row["rate"]),
                "total": _to_decimal(row["total"]),
                "editable": row["editable"],
                "daily_values": [
                    {
                        "date": item["date"],
                        "value": _to_decimal(item["value"]),
                        "editable": item["editable"],
                    }
                    for item in row["daily_values"]
                ],
            }
            for row in payload["rows"]
        ],
        "daily_totals": [
            {"date": item["date"], "value": _to_decimal(item["value"])}
            for item in payload["daily_totals"]
        ],
        "total_to_pay": _to_decimal(payload["total_to_pay"]),
        "week_corrida": _to_decimal(payload["week_corrida"]),
        "production_total": _to_decimal(payload["production_total"]),
    }


def build_settlement_payload(
    db: Session,
    *,
    cycle_id: int,
    employee_id: int,
    cost_center: str | None,
    role_type: str | None,
) -> dict[str, object]:
    try:
        payload = settlement_engine.build(
            db,
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=cost_center,
            role_type=role_type,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _serialize_settlement_payload(payload)


def log_export(
    db: Session,
    *,
    current_user: User,
    cycle_id: int,
    employee_id: int,
    cost_center: str | None,
    role_type: str | None,
    file_format: str,
    file_name: str,
) -> None:
    export_scope = "SEARCH" if cost_center is None or role_type is None else "SETTLEMENT"
    db.add(
        PayrollExportLog(
            user_id=current_user.id,
            export_scope=export_scope,
            file_format=file_format.upper(),
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=cost_center,
            role_type=role_type,
            file_name=file_name,
        )
    )
    db.commit()


def _frontend_asset_path(requested_path: str) -> Path | None:
    if not requested_path:
        return None
    candidate = (FRONTEND_BUILD_DIR / requested_path).resolve()
    try:
        candidate.relative_to(FRONTEND_BUILD_DIR.resolve())
    except ValueError:
        return None
    if candidate.is_file():
        return candidate
    return None


@app.get("/api/health")
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    check_connection(db)
    return {"status": "ok", "database": "connected"}


@app.post("/api/auth/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> LoginResponse:
    user = authenticate(db, payload.username, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña inválidos.",
        )
    token, expires_in = create_access_token(user.id, settings)
    return LoginResponse(
        access_token=token,
        expires_in=expires_in,
        user=serialize_user(user),
    )


@app.get("/api/auth/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)) -> UserResponse:
    return serialize_user(user)


@app.post("/api/email/test")
def email_test(
    settings: Settings = Depends(get_settings),
    _: User = Depends(require_permission("payroll.email")),
) -> dict[str, str]:
    try:
        recipient = send_test_email(settings)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except (OSError, smtplib.SMTPException) as exc:
        raise HTTPException(
            status_code=502,
            detail="El servidor de correo rechazó o no pudo completar el envío SMTP.",
        ) from exc
    return {"status": "sent", "recipient": recipient}


@app.post("/api/email/settlement")
def email_settlement(
    payload: SettlementEmailRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
    _: User = Depends(require_permission("payroll.email")),
) -> dict[str, str]:
    normalized_cost_center = normalize_cost_center(payload.cost_center)
    normalized_role_type = normalize_role_type(payload.role_type)
    settlement = build_settlement_payload(
        db,
        cycle_id=payload.cycle_id,
        employee_id=payload.employee_id,
        cost_center=normalized_cost_center,
        role_type=normalized_role_type,
    )
    recipient = str(settings.smtp_test_recipient or "").strip()
    recipient_name = "Destinatario de prueba"
    if not recipient:
        raise HTTPException(
            status_code=503,
            detail="No hay un destinatario de prueba configurado.",
        )
    file_name = export_file_name(
        settlement=settlement,
        file_format="pdf",
        cost_center=normalized_cost_center,
        role_type=normalized_role_type,
    )
    try:
        send_settlement_email(
            settings,
            recipient=recipient,
            recipient_name=recipient_name,
            pdf_content=export_pdf_bytes(settlement),
            pdf_file_name=file_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (OSError, smtplib.SMTPException) as exc:
        raise HTTPException(
            status_code=502,
            detail="El servidor de correo rechazó o no pudo completar el envío SMTP.",
        ) from exc
    return {"status": "sent", "recipient": recipient, "recipient_name": recipient_name}


@app.get("/api/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users.manage")),
) -> list[UserResponse]:
    users = db.scalars(select(User).order_by(User.username)).all()
    return [serialize_user(user) for user in users]


@app.get("/api/roles", response_model=list[RoleResponse])
def list_roles(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users.manage")),
) -> list[RoleResponse]:
    roles = db.scalars(
        select(Role).where(Role.active.is_(True)).order_by(Role.role_name)
    ).all()
    return [
        RoleResponse(
            role_name=role.role_name,
            description=role.description,
            active=role.active,
            permissions=sorted(item.permission_code for item in role.permissions),
        )
        for role in roles
    ]


@app.get("/api/permissions", response_model=list[PermissionResponse])
def list_permissions(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users.manage")),
) -> list[Permission]:
    return list(db.scalars(select(Permission).order_by(Permission.permission_code)).all())


@app.post("/api/users", response_model=UserResponse, status_code=201)
def add_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users.manage")),
) -> UserResponse:
    try:
        user = create_user(db, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return serialize_user(user)


@app.patch("/api/users/{user_id}/active", response_model=UserResponse)
def set_user_active(
    user_id: int,
    payload: UserActiveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.manage")),
) -> UserResponse:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if user.id == current_user.id and not payload.active:
        raise HTTPException(status_code=400, detail="No puede desactivar su usuario.")
    user.active = payload.active
    db.commit()
    return serialize_user(user)


@app.get("/api/cycles", response_model=list[CycleResponse])
def list_cycles(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.read")),
) -> list[PayrollCycle]:
    return list(db.scalars(select(PayrollCycle).order_by(PayrollCycle.start_date.desc())).all())


@app.get("/api/holidays", response_model=list[HolidayResponse])
def list_holidays(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.read")),
) -> list[HolidayResponse]:
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Mes invalido.")
    rows = holiday_service.list_month(db, year, month)
    if holiday_service.table_exists(db):
        db.commit()
    return [_serialize_holiday(row) for row in rows]


@app.post("/api/holidays", response_model=HolidayResponse, status_code=201)
def create_holiday(
    payload: HolidayCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> HolidayResponse:
    if current_user.role.role_name != "ADMIN":
        raise HTTPException(status_code=403, detail="Solo ADMIN puede editar feriados.")
    if not holiday_service.table_exists(db):
        raise HTTPException(status_code=400, detail="La base de datos no tiene habilitada la tabla payroll_holidays.")
    holiday = PayrollHoliday(
        holiday_date=payload.holiday_date,
        holiday_name=" ".join(payload.holiday_name.strip().split()),
        holiday_scope=normalize_holiday_scope(payload.holiday_scope),
        active=payload.active,
        is_default=False,
        created_by=current_user.id,
        updated_by=current_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(holiday)
    db.commit()
    db.refresh(holiday)
    return _serialize_holiday(holiday)


@app.put("/api/holidays/{holiday_id}", response_model=HolidayResponse)
def update_holiday(
    holiday_id: int,
    payload: HolidayUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> HolidayResponse:
    if current_user.role.role_name != "ADMIN":
        raise HTTPException(status_code=403, detail="Solo ADMIN puede editar feriados.")
    holiday = db.get(PayrollHoliday, holiday_id)
    if holiday is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado.")
    holiday.holiday_date = payload.holiday_date
    holiday.holiday_name = " ".join(payload.holiday_name.strip().split())
    holiday.holiday_scope = normalize_holiday_scope(payload.holiday_scope)
    holiday.active = payload.active
    holiday.updated_by = current_user.id
    holiday.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(holiday)
    return _serialize_holiday(holiday)


@app.get("/api/search/records", response_model=SearchResponse)
def search_records(
    cycle_from_id: int,
    cycle_to_id: int,
    cost_center: str | None = None,
    role_type: str | None = None,
    employee_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.read")),
) -> SearchResponse:
    cycle_from = db.get(PayrollCycle, cycle_from_id)
    cycle_to = db.get(PayrollCycle, cycle_to_id)
    if cycle_from is None or cycle_to is None:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado.")
    start_date = min(cycle_from.start_date, cycle_to.start_date)
    end_date = max(cycle_from.start_date, cycle_to.start_date)
    cycle_ids = list(
        db.scalars(
            select(PayrollCycle.id)
            .where(PayrollCycle.start_date.between(start_date, end_date))
            .order_by(PayrollCycle.start_date)
        ).all()
    )
    filters = [PayrollRecord.cycle_id.in_(cycle_ids)]
    if cost_center:
        normalized_cost_center = cost_center.upper()
        if normalized_cost_center != "ALL":
            if normalized_cost_center not in {"DR", "SERVICES"}:
                raise HTTPException(status_code=400, detail="Centro de costo invalido.")
            filters.append(PayrollRecord.cost_center == normalized_cost_center)
    if role_type:
        normalized_role_type = role_type.upper()
        if normalized_role_type != "ALL":
            if normalized_role_type not in {"DRIVER", "ASSISTANT"}:
                raise HTTPException(status_code=400, detail="Cargo invalido.")
            filters.append(PayrollRecord.role_type == normalized_role_type)
    if employee_id:
        filters.append(PayrollRecord.employee_id == employee_id)
    count = db.scalar(select(func.count(PayrollRecord.id)).where(*filters))
    return SearchResponse(cycle_ids=cycle_ids, records_count=count or 0)


@app.get("/api/search/employees", response_model=list[SearchEmployeeOptionResponse])
def search_employee_options(
    cycle_from_id: int,
    cycle_to_id: int,
    cost_center: str | None = None,
    role_type: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.read")),
) -> list[SearchEmployeeOptionResponse]:
    cycle_from = db.get(PayrollCycle, cycle_from_id)
    cycle_to = db.get(PayrollCycle, cycle_to_id)
    if cycle_from is None or cycle_to is None:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado.")
    start_date = min(cycle_from.start_date, cycle_to.start_date)
    end_date = max(cycle_from.start_date, cycle_to.start_date)
    cycle_ids = list(
        db.scalars(
            select(PayrollCycle.id)
            .where(PayrollCycle.start_date.between(start_date, end_date))
            .order_by(PayrollCycle.start_date)
        ).all()
    )
    filters = [PayrollRecord.cycle_id.in_(cycle_ids)]
    if cost_center:
        normalized_cost_center = cost_center.upper()
        if normalized_cost_center != "ALL":
            if normalized_cost_center not in {"DR", "SERVICES"}:
                raise HTTPException(status_code=400, detail="Centro de costo invalido.")
            filters.append(PayrollRecord.cost_center == normalized_cost_center)
    if role_type:
        normalized_role_type = role_type.upper()
        if normalized_role_type != "ALL":
            if normalized_role_type not in {"DRIVER", "ASSISTANT"}:
                raise HTTPException(status_code=400, detail="Cargo invalido.")
            filters.append(PayrollRecord.role_type == normalized_role_type)
    employees = list(
        db.scalars(
            select(Employee)
            .join(PayrollRecord, PayrollRecord.employee_id == Employee.id)
            .where(*filters)
            .order_by(Employee.id)
        ).all()
    )
    grouped: dict[str, list[Employee]] = {}
    for employee in employees:
        key = normalize_employee_name(employee.employee_name)
        grouped.setdefault(key, []).append(employee)
    rows = []
    for matches in grouped.values():
        worker = min(matches, key=lambda item: item.id)
        rows.append(
            SearchEmployeeOptionResponse(
                id=worker.id,
                employee_name=worker.employee_name,
                contract_type=next((item.contract_type for item in matches if item.contract_type), None),
                rut=next((item.rut for item in matches if item.rut), None),
                email=next((item.email for item in matches if item.email), None),
                cargo=next((item.cargo for item in matches if item.cargo), None),
            )
        )
    return sorted(rows, key=lambda item: item.employee_name)


@app.get("/api/settlements/employees", response_model=list[EmployeeOptionResponse])
def list_settlement_employees(
    cycle_id: int,
    cost_center: str,
    role_type: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.read")),
) -> list[EmployeeOptionResponse]:
    normalized_cost_center = cost_center.upper()
    normalized_role_type = role_type.upper()
    if normalized_cost_center not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Centro de costo invalido.")
    if normalized_role_type not in {"DRIVER", "ASSISTANT"}:
        raise HTTPException(status_code=400, detail="Cargo invalido.")
    return list(
        settlement_engine.list_employees(
            db,
            cycle_id=cycle_id,
            cost_center=normalized_cost_center,
            role_type=normalized_role_type,
        )
    )


@app.get("/api/workers", response_model=list[WorkerListItemResponse])
def list_workers(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("workers.read")),
) -> list[WorkerListItemResponse]:
    employees = list(db.scalars(select(Employee).order_by(Employee.id)).all())
    grouped: dict[str, list[Employee]] = {}
    for employee in employees:
        key = normalize_employee_name(employee.employee_name)
        grouped.setdefault(key, []).append(employee)
    rows = []
    for matches in grouped.values():
        worker = min(matches, key=lambda item: item.id)
        rows.append(
            WorkerListItemResponse(
                id=worker.id,
                employee_name=grouped_employee_display_name(matches),
                contract_type=next((item.contract_type for item in matches if item.contract_type), None),
                rut=next((item.rut for item in matches if item.rut), None),
                email=next((item.email for item in matches if item.email), None),
                cargo=next((item.cargo for item in matches if item.cargo), None),
            )
        )
    return sorted(rows, key=lambda item: item.employee_name)


@app.post("/api/workers", response_model=WorkerListItemResponse, status_code=201)
def create_worker(
    payload: WorkerCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("workers.edit")),
) -> WorkerListItemResponse:
    employee_name = " ".join(payload.employee_name.strip().split())
    if not employee_name:
        raise HTTPException(status_code=400, detail="Nombre de trabajador requerido.")
    contract_type = normalize_contract_type(payload.contract_type)
    rut = normalize_rut(payload.rut)
    email = normalize_email(payload.email)
    cargo = normalize_cargo(payload.cargo)
    matches = find_related_employees_by_name(db, employee_name)
    if matches:
        for employee in matches:
            employee.contract_type = contract_type
            employee.rut = rut
            employee.email = email
            employee.cargo = cargo
            if not employee.first_name and not employee.paternal_surname:
                apply_employee_name_parts(employee, employee_name)
        db.commit()
        worker = min(matches, key=lambda item: item.id)
        return WorkerListItemResponse(
            id=worker.id,
            employee_name=grouped_employee_display_name(matches),
            contract_type=contract_type,
            rut=rut,
            email=email,
            cargo=cargo,
        )
    worker = Employee(
        employee_name=employee_name,
        role_type="UNASSIGNED",
        contract_type=contract_type,
        rut=rut,
        email=email,
        cargo=cargo,
    )
    apply_employee_name_parts(worker, employee_name)
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return WorkerListItemResponse(
        id=worker.id,
        employee_name=employee_display_name(worker),
        contract_type=worker.contract_type,
        rut=worker.rut,
        email=worker.email,
        cargo=worker.cargo,
    )


@app.put("/api/workers/{worker_id}", response_model=WorkerListItemResponse)
def update_worker(
    worker_id: int,
    payload: WorkerUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("workers.edit")),
) -> WorkerListItemResponse:
    worker = db.get(Employee, worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")
    contract_type = normalize_contract_type(payload.contract_type)
    rut = normalize_rut(payload.rut)
    email = normalize_email(payload.email)
    cargo = normalize_cargo(payload.cargo)
    matches = find_related_employees_by_name(db, worker.employee_name)
    for employee in matches:
        employee.contract_type = contract_type
        employee.rut = rut
        employee.email = email
        employee.cargo = cargo
        if not employee.first_name and not employee.paternal_surname:
            apply_employee_name_parts(employee, employee.employee_name)
    db.commit()
    return WorkerListItemResponse(
        id=worker.id,
        employee_name=grouped_employee_display_name(matches),
        contract_type=contract_type,
        rut=rut,
        email=email,
        cargo=cargo,
    )


@app.delete("/api/workers/{worker_id}", status_code=204)
def delete_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("workers.edit")),
) -> Response:
    worker = db.get(Employee, worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")

    matches = find_related_employees_by_name(db, worker.employee_name)
    employee_ids = [employee.id for employee in matches]
    has_records = db.scalar(
        select(func.count()).select_from(PayrollRecord).where(PayrollRecord.employee_id.in_(employee_ids))
    )
    has_adjustments = db.scalar(
        select(func.count()).select_from(PayrollManualAdjustment).where(
            PayrollManualAdjustment.employee_id.in_(employee_ids)
        )
    )
    has_overrides = db.scalar(
        select(func.count()).select_from(PayrollCellOverride).where(
            PayrollCellOverride.employee_id.in_(employee_ids)
        )
    )
    if (has_records or 0) > 0 or (has_adjustments or 0) > 0 or (has_overrides or 0) > 0:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el trabajador porque tiene registros historicos asociados.",
        )
    for employee in matches:
        db.delete(employee)
    db.commit()
    return Response(status_code=204)


@app.get("/api/manual-adjustments", response_model=list[ManualAdjustmentResponse])
def list_manual_adjustments(
    cycle_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.read")),
) -> list[ManualAdjustmentResponse]:
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")
    related_employee_ids = [
        item.id
        for item in db.scalars(select(Employee).order_by(Employee.id)).all()
        if names_refer_to_same_person(item.employee_name, employee.employee_name)
    ]
    adjustments = list(
        db.scalars(
            select(PayrollManualAdjustment)
            .where(PayrollManualAdjustment.cycle_id == cycle_id)
            .where(PayrollManualAdjustment.employee_id.in_(related_employee_ids))
            .where(PayrollManualAdjustment.active.is_(True))
            .order_by(PayrollManualAdjustment.id.desc())
        ).all()
    )
    history_map = _history_rows_for_adjustments(db, [item.id for item in adjustments])
    return [
        _serialize_adjustment(adjustment, history_map.get(adjustment.id, []))
        for adjustment in adjustments
    ]


@app.post("/api/manual-adjustments", response_model=ManualAdjustmentResponse, status_code=201)
def create_manual_adjustment(
    payload: ManualAdjustmentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> ManualAdjustmentResponse:
    employee = db.get(Employee, payload.employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")
    now = datetime.utcnow()
    adjustment = PayrollManualAdjustment(
        cycle_id=payload.cycle_id,
        employee_id=payload.employee_id,
        cost_center="ALL",
        role_type="ALL",
        adjustment_type=normalize_adjustment_type(payload.adjustment_type),
        adjustment_name=effective_adjustment_name(
            payload.adjustment_type,
            payload.description,
        ),
        units=payload.units,
        amount=payload.amount,
        notes=payload.observations.strip() if payload.observations else None,
        active=True,
        created_by=current_user.id,
        updated_by=current_user.id,
        created_at=now,
        updated_at=now,
    )
    db.add(adjustment)
    db.flush()
    db.add(
        PayrollAuditLog(
            user_id=current_user.id,
            action_type="CREATE_MANUAL_ADJUSTMENT",
            table_name="payroll_manual_adjustments",
            record_id=adjustment.id,
            old_value=None,
            new_value=json.dumps(
                {
                    "adjustment_type": adjustment.adjustment_type,
                    "description": adjustment.adjustment_name,
                    "units": str(adjustment.units) if adjustment.units is not None else None,
                    "amount": str(adjustment.amount),
                    "observations": adjustment.notes,
                    "active": adjustment.active,
                },
                ensure_ascii=True,
            ),
        )
    )
    db.commit()
    history_map = _history_rows_for_adjustments(db, [adjustment.id])
    return _serialize_adjustment(adjustment, history_map.get(adjustment.id, []))


@app.put("/api/manual-adjustments/{adjustment_id}", response_model=ManualAdjustmentResponse)
def update_manual_adjustment(
    adjustment_id: int,
    payload: ManualAdjustmentUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> ManualAdjustmentResponse:
    adjustment = db.get(PayrollManualAdjustment, adjustment_id)
    if adjustment is None:
        raise HTTPException(status_code=404, detail="Ajuste no encontrado.")
    old_snapshot = {
        "adjustment_type": adjustment.adjustment_type,
        "description": adjustment.adjustment_name,
        "units": str(adjustment.units) if adjustment.units is not None else None,
        "amount": str(adjustment.amount),
        "observations": adjustment.notes,
        "active": adjustment.active,
    }
    adjustment.adjustment_type = normalize_adjustment_type(payload.adjustment_type)
    adjustment.adjustment_name = effective_adjustment_name(
        payload.adjustment_type,
        payload.description,
    )
    adjustment.units = payload.units
    adjustment.amount = payload.amount
    adjustment.notes = payload.observations.strip() if payload.observations else None
    adjustment.updated_by = current_user.id
    adjustment.updated_at = datetime.utcnow()
    db.add(
        PayrollAuditLog(
            user_id=current_user.id,
            action_type="UPDATE_MANUAL_ADJUSTMENT",
            table_name="payroll_manual_adjustments",
            record_id=adjustment.id,
            old_value=json.dumps(old_snapshot, ensure_ascii=True),
            new_value=json.dumps(
                {
                    "adjustment_type": adjustment.adjustment_type,
                    "description": adjustment.adjustment_name,
                    "units": str(adjustment.units) if adjustment.units is not None else None,
                    "amount": str(adjustment.amount),
                    "observations": adjustment.notes,
                    "active": adjustment.active,
                },
                ensure_ascii=True,
            ),
        )
    )
    db.commit()
    history_map = _history_rows_for_adjustments(db, [adjustment.id])
    return _serialize_adjustment(adjustment, history_map.get(adjustment.id, []))


@app.delete("/api/manual-adjustments/{adjustment_id}", response_model=ManualAdjustmentResponse)
def delete_manual_adjustment(
    adjustment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> ManualAdjustmentResponse:
    adjustment = db.get(PayrollManualAdjustment, adjustment_id)
    if adjustment is None:
        raise HTTPException(status_code=404, detail="Ajuste no encontrado.")
    old_snapshot = {
        "adjustment_type": adjustment.adjustment_type,
        "description": adjustment.adjustment_name,
        "units": str(adjustment.units) if adjustment.units is not None else None,
        "amount": str(adjustment.amount),
        "observations": adjustment.notes,
        "active": adjustment.active,
    }
    adjustment.active = False
    adjustment.updated_by = current_user.id
    adjustment.updated_at = datetime.utcnow()
    adjustment.deleted_at = adjustment.updated_at
    db.add(
        PayrollAuditLog(
            user_id=current_user.id,
            action_type="DELETE_MANUAL_ADJUSTMENT",
            table_name="payroll_manual_adjustments",
            record_id=adjustment.id,
            old_value=json.dumps(old_snapshot, ensure_ascii=True),
            new_value=json.dumps(
                {
                    **old_snapshot,
                    "active": False,
                    "deleted_at": adjustment.deleted_at.isoformat() if adjustment.deleted_at else None,
                },
                ensure_ascii=True,
            ),
        )
    )
    db.commit()
    history_map = _history_rows_for_adjustments(db, [adjustment.id])
    return _serialize_adjustment(adjustment, history_map.get(adjustment.id, []))


@app.get("/api/settlements", response_model=SettlementResponse)
def get_settlement(
    cycle_id: int,
    employee_id: int,
    cost_center: Annotated[str | None, Query()] = None,
    role_type: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.read")),
) -> SettlementResponse:
    normalized_cost_center = cost_center.upper() if cost_center else None
    normalized_role_type = role_type.upper() if role_type else None
    if normalized_cost_center in {"ALL", "CONSOLIDATED"}:
        normalized_cost_center = None
    if normalized_role_type in {"ALL", "CONSOLIDATED"}:
        normalized_role_type = None
    if normalized_cost_center is not None and normalized_cost_center not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Centro de costo invalido.")
    if normalized_role_type is not None and normalized_role_type not in {"DRIVER", "ASSISTANT"}:
        raise HTTPException(status_code=400, detail="Cargo invalido.")
    try:
        result = settlement_engine.build(
            db,
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=normalized_cost_center,
            role_type=normalized_role_type,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SettlementResponse.model_validate(result)


@app.get("/api/liquidations", response_model=SettlementResponse)
def get_liquidation(
    cycle_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.read")),
) -> SettlementResponse:
    try:
        result = settlement_engine.build(
            db,
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=None,
            role_type=None,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SettlementResponse.model_validate(result)


@app.get("/api/exports/settlement")
def export_settlement(
    cycle_id: int,
    employee_id: int,
    file_format: str,
    cost_center: Annotated[str | None, Query()] = None,
    role_type: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.export")),
) -> Response:
    normalized_cost_center = cost_center.upper() if cost_center else None
    normalized_role_type = role_type.upper() if role_type else None
    if normalized_cost_center in {"ALL", "CONSOLIDATED"}:
        normalized_cost_center = None
    if normalized_role_type in {"ALL", "CONSOLIDATED"}:
        normalized_role_type = None
    normalized_cost_center = normalize_cost_center(normalized_cost_center)
    normalized_role_type = normalize_role_type(normalized_role_type)
    normalized_format = file_format.strip().lower()
    if normalized_format not in {"xlsx", "csv", "pdf"}:
        raise HTTPException(status_code=400, detail="Formato de exportacion invalido.")

    settlement = build_settlement_payload(
        db,
        cycle_id=cycle_id,
        employee_id=employee_id,
        cost_center=normalized_cost_center,
        role_type=normalized_role_type,
    )
    file_name = export_file_name(
        settlement=settlement,
        file_format=normalized_format,
        cost_center=normalized_cost_center,
        role_type=normalized_role_type,
    )
    content = (
        export_xlsx_bytes(settlement)
        if normalized_format == "xlsx"
        else export_pdf_bytes(settlement)
        if normalized_format == "pdf"
        else export_csv_bytes(settlement)
    )
    log_export(
        db,
        current_user=current_user,
        cycle_id=cycle_id,
        employee_id=employee_id,
        cost_center=normalized_cost_center,
        role_type=normalized_role_type,
        file_format=normalized_format,
        file_name=file_name,
    )
    media_type = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if normalized_format == "xlsx"
        else "application/pdf"
        if normalized_format == "pdf"
        else "text/csv; charset=utf-8"
    )
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@app.post("/api/settlements/rates", response_model=SettlementResponse)
def update_settlement_rates(
    payload: SettlementRateUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rates.edit")),
) -> SettlementResponse:
    normalized_cost_center = payload.cost_center.upper()
    normalized_role_type = payload.role_type.upper()
    if normalized_cost_center not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Centro de costo invalido.")
    if normalized_role_type not in {"DRIVER", "ASSISTANT"}:
        raise HTTPException(status_code=400, detail="Cargo invalido.")
    if len({item.concept_id for item in payload.updates}) != len(payload.updates):
        raise HTTPException(status_code=400, detail="No repita conceptos en la solicitud.")
    try:
        employee = db.get(Employee, payload.employee_id)
        if employee is None:
            raise LookupError("Trabajador no encontrado.")
        related_employees = [
            item
            for item in db.scalars(select(Employee).order_by(Employee.id)).all()
            if names_refer_to_same_person(item.employee_name, employee.employee_name)
        ]
        contract_type = next((item.contract_type for item in related_employees if item.contract_type), None)
        concept_rate_service.create_versions(
            db,
            cycle_id=payload.cycle_id,
            cost_center=normalized_cost_center,
            role_type=normalized_role_type,
            contract_type=contract_type,
            updates=[
                (item.concept_id, item.amount, item.apply_mode)
                for item in payload.updates
            ],
            admin=current_user,
        )
        db.flush()
        result = settlement_engine.build(
            db,
            cycle_id=payload.cycle_id,
            employee_id=payload.employee_id,
            cost_center=normalized_cost_center,
            role_type=normalized_role_type,
        )
        db.commit()
    except LookupError as exc:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SettlementResponse.model_validate(result)


@app.post("/api/liquidations/cells", response_model=SettlementResponse)
def update_liquidation_cells(
    payload: SettlementCellUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> SettlementResponse:
    try:
        result = settlement_engine.update_daily_cells(
            db,
            cycle_id=payload.cycle_id,
            employee_id=payload.employee_id,
            cost_center=None,
            role_type=None,
            updates=[
                (item.concept_id, item.work_date, item.value)
                for item in payload.updates
            ],
            user_id=current_user.id,
        )
        db.commit()
    except LookupError as exc:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SettlementResponse.model_validate(result)


@app.post("/api/settlements/cells", response_model=SettlementResponse)
def update_settlement_cells(
    payload: SettlementCellUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> SettlementResponse:
    normalized_cost_center = payload.cost_center.upper() if payload.cost_center else None
    normalized_role_type = payload.role_type.upper() if payload.role_type else None
    if normalized_cost_center in {"ALL", "CONSOLIDATED"}:
        normalized_cost_center = None
    if normalized_role_type in {"ALL", "CONSOLIDATED"}:
        normalized_role_type = None
    if normalized_cost_center is not None and normalized_cost_center not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Centro de costo invalido.")
    if normalized_role_type is not None and normalized_role_type not in {"DRIVER", "ASSISTANT"}:
        raise HTTPException(status_code=400, detail="Cargo invalido.")
    try:
        result = settlement_engine.update_daily_cells(
            db,
            cycle_id=payload.cycle_id,
            employee_id=payload.employee_id,
            cost_center=normalized_cost_center,
            role_type=normalized_role_type,
            updates=[
                (item.concept_id, item.work_date, item.value)
                for item in payload.updates
            ],
            user_id=current_user.id,
        )
        db.commit()
    except LookupError as exc:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SettlementResponse.model_validate(result)


@app.get("/api/rates", response_model=list[RateListItemResponse])
def list_rates(
    cost_center: str,
    role_type: str,
    cycle_id: int,
    contract_type: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("rates.read")),
) -> list[RateListItemResponse]:
    normalized_cost_center = cost_center.upper()
    normalized_role_type = role_type.upper()
    if normalized_cost_center not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Centro de costo invalido.")
    if normalized_role_type not in {"DRIVER", "ASSISTANT"}:
        raise HTTPException(status_code=400, detail="Cargo invalido.")
    try:
        rows = concept_rate_service.list_rates(
            db,
            cost_center=normalized_cost_center,
            role_type=normalized_role_type,
            cycle_id=cycle_id,
            contract_type=normalize_contract_type(contract_type),
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return [RateListItemResponse.model_validate(row.__dict__) for row in rows]


@app.post("/api/rates", response_model=RateListItemResponse, status_code=201)
def create_rate(
    payload: RateCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rates.edit")),
) -> RateListItemResponse:
    try:
        rate = concept_rate_service.save_rate(
            db,
            concept_id=payload.concept_id,
            cycle_id=payload.cycle_id,
            amount=payload.amount,
            apply_mode=payload.apply_mode,
            contract_type=normalize_contract_type(payload.contract_type),
            admin=current_user,
        )
        concept = concept_rate_service.concept(db, concept_id=payload.concept_id)
    except LookupError as exc:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    db.commit()
    row = next(
        item
        for item in concept_rate_service.list_rates(
            db,
            cost_center=concept.cost_center,
            role_type=concept.role_type,
            cycle_id=payload.cycle_id,
            contract_type=normalize_contract_type(payload.contract_type),
        )
        if item.concept_id == payload.concept_id
    )
    return RateListItemResponse.model_validate(row.__dict__)


@app.put("/api/rates/{rate_id}", response_model=RateListItemResponse)
def update_rate(
    rate_id: int,
    payload: RateUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rates.edit")),
) -> RateListItemResponse:
    try:
        rate = concept_rate_service.update_rate(
            db,
            rate_id=rate_id,
            cycle_id=payload.cycle_id,
            amount=payload.amount,
            apply_mode=payload.apply_mode,
            contract_type=normalize_contract_type(payload.contract_type),
            admin=current_user,
        )
    except LookupError as exc:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    db.commit()
    _, concept = concept_rate_service.rate_context(db, rate_id=rate.id)
    rows = concept_rate_service.list_rates(
        db,
        cost_center=concept.cost_center,
        role_type=concept.role_type,
        cycle_id=payload.cycle_id,
        contract_type=normalize_contract_type(payload.contract_type),
    )
    row = next(item for item in rows if item.concept_id == concept.id)
    return RateListItemResponse.model_validate(row.__dict__)


@app.get("/api/imports", response_model=list[ImportHistoryResponse])
def list_imports(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("payroll.import")),
) -> list[ImportHistoryResponse]:
    rows = db.execute(
        select(PayrollImport, User.username)
        .join(User, User.id == PayrollImport.imported_by)
        .order_by(PayrollImport.imported_at.desc())
        .limit(100)
    ).all()
    return [
        ImportHistoryResponse(
            id=payroll_import.id,
            imported_at=payroll_import.imported_at,
            file_name=payroll_import.file_name,
            source_type=payroll_import.source_type,
            rows_imported=payroll_import.rows_imported,
            imported_by=username,
        )
        for payroll_import, username in rows
    ]


@app.post("/api/imports/{source_type}", response_model=ImportResponse)
async def import_excel(
    source_type: str,
    confirm_reimport: bool = Form(False),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.import")),
) -> ImportResponse:
    normalized_source = source_type.upper()
    if normalized_source not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Tipo de importación inválido.")
    if not file.filename or not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Debe seleccionar un archivo .xlsx.")
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="El archivo excede el máximo de 50 MB.")
    try:
        cycles, cycles_created = ensure_workbook_cycles(db, content, normalized_source)
        parsed = parse_workbook(content, normalized_source, cycles)
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not parsed.candidates:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "message": "El archivo no contiene registros importables para el ciclo.",
                "rows_read": parsed.rows_read,
                "rows_outside_cycle": parsed.rows_outside_cycle,
                "errors": parsed.errors,
            },
        )
    possible_reimports = find_possible_reimports(
        db,
        normalized_source,
        parsed.candidates,
    )
    if possible_reimports and not confirm_reimport:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail={
                "requires_confirmation": True,
                "message": (
                    "Se detectaron posibles registros reimportados. "
                    "Confirme explícitamente para insertarlos."
                ),
                "possible_reimports": len(possible_reimports),
                "rows_read": parsed.rows_read,
                "records_ready": len(parsed.candidates),
                "rows_outside_cycle": parsed.rows_outside_cycle,
                "errors": parsed.errors,
            },
        )
    try:
        payroll_imports, workers_created = persist_import(
            db,
            parsed,
            current_user,
            file.filename,
        )
    except Exception:
        db.rollback()
        raise
    return ImportResponse(
        import_ids=[item.id for item in payroll_imports],
        file_name=file.filename,
        source_type=normalized_source,
        cycle_ids=sorted({candidate.values["cycle_id"] for candidate in parsed.candidates}),
        cycles_created=cycles_created,
        rows_read=parsed.rows_read,
        records_inserted=len(parsed.candidates),
        workers_created=workers_created,
        rows_outside_cycle=parsed.rows_outside_cycle,
        errors=parsed.errors,
        possible_reimports_confirmed=len(possible_reimports),
    )


if FRONTEND_ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_ASSETS_DIR), name="frontend-assets")


@app.get("/", include_in_schema=False)
def frontend_index() -> FileResponse:
    index_file = FRONTEND_BUILD_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend publicado no encontrado.")
    return FileResponse(index_file)


@app.get("/{full_path:path}", include_in_schema=False)
def frontend_spa_fallback(full_path: str) -> Response:
    blocked_prefixes = ("api/", "docs", "redoc", "openapi.json")
    if full_path in {"api", "docs", "redoc", "openapi.json"} or full_path.startswith(blocked_prefixes):
        raise HTTPException(status_code=404, detail="No encontrado.")
    asset_path = _frontend_asset_path(full_path)
    if asset_path is not None:
        return FileResponse(asset_path)
    index_file = FRONTEND_BUILD_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend publicado no encontrado.")
    return FileResponse(index_file)
