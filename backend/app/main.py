from __future__ import annotations

import json
import smtplib
from contextlib import asynccontextmanager
from datetime import UTC, date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Annotated
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy import delete, func, inspect, select, text
from sqlalchemy.exc import IntegrityError
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
from .exporter import (
    export_audit_pdf_bytes,
    export_csv_bytes,
    export_file_name,
    export_pdf_bytes,
    export_sheet_pdf_bytes,
    export_softland_xlsx_bytes,
    export_xlsx_bytes,
)
from .holidays import ALLOWED_HOLIDAY_SCOPES, HolidayService
from .importer import ensure_workbook_cycles, find_possible_reimports, parse_workbook, persist_import
from .models import (
    Employee,
    PayrollAuditLog,
    PayrollCycle,
    PayrollExportLog,
    PayrollHoliday,
    PayrollImport,
    PayrollIpcAdjustment,
    PayrollManualAdjustment,
    PayrollConceptRate,
    PayrollRecord,
    PayrollSetting,
    PayrollCellOverride,
    Permission,
    Role,
    User,
)
from .rates import ConceptRateService
from .schemas import (
    CycleResponse,
    AuditEntryResponse,
    EmployeeOptionResponse,
    HolidayCreateRequest,
    HolidayResponse,
    HolidayUpdateRequest,
    ImportHistoryResponse,
    ImportCycleDeleteResponse,
    ImportResponse,
    IpcAdjustmentCreateRequest,
    IpcAdjustmentResponse,
    LoginRequest,
    LoginResponse,
    ManualAdjustmentCreateRequest,
    ManualAdjustmentResponse,
    ManualAdjustmentUpdateRequest,
    ManualAdjustmentAuditResponse,
    OperationsEditLockResponse,
    OperationsEditLockUpdate,
    PermissionResponse,
    RateCreateRequest,
    RateListItemResponse,
    RateUpdateRequest,
    RoleResponse,
    SearchEmployeeOptionResponse,
    SearchResponse,
    SettlementCellUpdateRequest,
    SettlementStatusUpdateRequest,
    SettlementEmailRequest,
    SettlementResponse,
    SettlementRateUpdateRequest,
    WorkerCreateRequest,
    WorkerListItemResponse,
    WorkerUpdateRequest,
    UserActiveUpdate,
    UserCreate,
    UserPasswordReset,
    UserResponse,
    UserUpdate,
)
from .security import create_access_token, hash_password
from .settlements import SettlementEngine
from .softland import build_softland_rows, ensure_softland_mappings
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
        PayrollHoliday.__table__.create(bind=target_engine, checkfirst=True)
        PayrollSetting.__table__.create(bind=target_engine, checkfirst=True)
        with Session(target_engine) as db:
            seed_roles_and_permissions(db)
        return

    Base.metadata.create_all(target_engine)
    ensure_local_sqlite_extensions(target_engine)
    with Session(target_engine) as db:
        seed_roles_and_permissions(db)
        apply_base_concepts(db)
        ensure_softland_mappings(db)
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
    ipc_columns = {
        column["name"] for column in inspector.get_columns("payroll_ipc_adjustments")
    }
    statements: list[str] = []
    if "contract_type" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN contract_type VARCHAR(16) NULL"
        )
    if "cost_center" not in employee_columns:
        statements.append(
            "ALTER TABLE payroll_employees ADD COLUMN cost_center VARCHAR(32) NULL"
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
    if "effective_from_cycle_id" not in ipc_columns:
        statements.append(
            "ALTER TABLE payroll_ipc_adjustments ADD COLUMN effective_from_cycle_id INTEGER NULL"
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
        connection.execute(
            text(
                "UPDATE payroll_ipc_adjustments SET effective_from_cycle_id = "
                "(SELECT id FROM payroll_cycles ORDER BY start_date ASC, id ASC LIMIT 1) "
                "WHERE effective_from_cycle_id IS NULL"
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


def normalize_worker_cost_center(cost_center: str | None) -> str | None:
    if cost_center is None:
        return None
    normalized = cost_center.strip().upper()
    if normalized not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Centro de costo inválido.")
    return normalized


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
    allowed = {
        "VACATION",
        "VACATION_BONUS",
        "PRODUCTION_BONUS",
        "EVENT_BONUS",
    }
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
        "VACATION_BONUS": "Bono Vacaciones",
        "PRODUCTION_BONUS": "Bono Producción",
        "EVENT_BONUS": "Bono Evento",
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
    export_scope_override: str | None = None,
) -> None:
    export_scope = export_scope_override or (
        "SEARCH" if cost_center is None or role_type is None else "SETTLEMENT"
    )
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


def _can_control_operations_edit_lock(user: User) -> bool:
    normalized_role = "".join(user.role.role_name.strip().upper().split())
    permissions = {item.permission_code for item in user.role.permissions}
    return (
        normalized_role in {"ADMIN", "ADMINISTRADOR", "RRHH", "RECURSOSHUMANOS"}
        or "users.manage" in permissions
        or {"rates.edit", "workers.edit"}.issubset(permissions)
    )


@app.get("/api/settings/operations-edit-lock", response_model=OperationsEditLockResponse)
def get_operations_edit_lock(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.read")),
) -> OperationsEditLockResponse:
    can_control = _can_control_operations_edit_lock(current_user)
    setting = db.scalar(
        select(PayrollSetting).where(
            PayrollSetting.setting_key == "operations_edit_locked"
        )
    )
    if setting is None:
        return OperationsEditLockResponse(locked=False, can_control=can_control)
    updated_by = None
    if setting.updated_by is not None:
        updated_by = db.scalar(select(User.full_name).where(User.id == setting.updated_by))
    return OperationsEditLockResponse(
        locked=setting.setting_value.casefold() == "true",
        can_control=can_control,
        updated_by=updated_by,
        updated_at=setting.updated_at,
    )


@app.put("/api/settings/operations-edit-lock", response_model=OperationsEditLockResponse)
def update_operations_edit_lock(
    payload: OperationsEditLockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.read")),
) -> OperationsEditLockResponse:
    if not _can_control_operations_edit_lock(current_user):
        raise HTTPException(
            status_code=403,
            detail="Solo ADMIN o RRHH puede bloquear o desbloquear las planillas.",
        )
    setting = db.scalar(
        select(PayrollSetting).where(
            PayrollSetting.setting_key == "operations_edit_locked"
        )
    )
    old_value = setting.setting_value if setting is not None else "false"
    new_value = "true" if payload.locked else "false"
    if setting is None:
        setting = PayrollSetting(
            setting_key="operations_edit_locked",
            setting_value=new_value,
        )
        db.add(setting)
        db.flush()
    setting.setting_value = new_value
    setting.updated_by = current_user.id
    setting.updated_at = datetime.utcnow()
    db.add(
        PayrollAuditLog(
            user_id=current_user.id,
            action_type="UPDATE_OPERATIONS_EDIT_LOCK",
            table_name="payroll_settings",
            record_id=setting.id,
            field_name="operations_edit_locked",
            old_value=old_value,
            new_value=new_value,
        )
    )
    db.commit()
    return OperationsEditLockResponse(
        locked=payload.locked,
        can_control=True,
        updated_by=current_user.full_name,
        updated_at=setting.updated_at,
    )


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


AUDIT_ACTION_LABELS = {
    "CREATE_HOLIDAY": "Agregó un feriado",
    "UPDATE_HOLIDAY": "Editó un feriado",
    "DELETE_IMPORTED_CYCLE": "Eliminó un ciclo importado",
    "UPDATE_DAILY_CELL_OVERRIDE": "Editó una planilla",
    "UPDATE_DAILY_STATUS": "Editó el estado de una planilla",
    "CREATE_MANUAL_ADJUSTMENT": "Agregó un ajuste a una planilla",
    "UPDATE_MANUAL_ADJUSTMENT": "Editó un ajuste de planilla",
    "DELETE_MANUAL_ADJUSTMENT": "Eliminó un ajuste de planilla",
    "CREATE_RATE": "Agregó una tarifa",
    "UPDATE_RATE": "Editó una tarifa",
    "RATE_RANGE_CLOSED": "Editó una tarifa",
    "RATE_SINGLE_CYCLE_REPLACED": "Editó una tarifa",
    "RATE_SINGLE_CYCLE_CREATED": "Editó una tarifa",
    "RATE_FORWARD_DEACTIVATED": "Editó una tarifa",
    "RATE_FORWARD_CREATED": "Editó una tarifa",
    "APPLY_IPC_ADJUSTMENT": "Aplicó una modificación IPC",
    "RESTORE_IPC_ADJUSTMENT": "Restauró tarifas desde un ajuste IPC",
    "CREATE_IPC_ADJUSTMENT": "Agregó una modificación IPC",
    "UPDATE_IPC_ADJUSTMENT": "Editó una modificación IPC",
    "CREATE_WORKER": "Agregó un trabajador",
    "UPDATE_WORKER": "Editó un trabajador",
    "DELETE_WORKER": "Eliminó un trabajador",
    "CREATE_USER": "Agregó un usuario",
    "UPDATE_USER": "Editó un usuario",
    "RESET_USER_PASSWORD": "Restableció la clave de un usuario",
    "DELETE_USER": "Eliminó un usuario",
    "SEND_EMAIL": "Envió una planilla o liquidación por email",
    "UPDATE_OPERATIONS_EDIT_LOCK": "Cambió el bloqueo de edición de planillas",
}

try:
    CHILE_TIMEZONE = ZoneInfo("America/Santiago")
except ZoneInfoNotFoundError:
    # Windows installations without the optional tzdata package. Azure Linux
    # provides the IANA database; this fallback preserves Chilean standard time locally.
    CHILE_TIMEZONE = timezone(timedelta(hours=-4), name="America/Santiago")


def _audit_day_utc_bounds(audit_date: date) -> tuple[datetime, datetime]:
    local_start = datetime.combine(audit_date, datetime.min.time(), tzinfo=CHILE_TIMEZONE)
    local_end = local_start + timedelta(days=1)
    return (
        local_start.astimezone(UTC).replace(tzinfo=None),
        local_end.astimezone(UTC).replace(tzinfo=None),
    )


def _audit_datetime_in_chile(value: datetime) -> datetime:
    utc_value = value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
    return utc_value.astimezone(CHILE_TIMEZONE).replace(tzinfo=None)


@app.get("/api/audit", response_model=list[AuditEntryResponse])
def list_audit_entries(
    audit_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.manage")),
) -> list[AuditEntryResponse]:
    if current_user.role.role_name != "ADMIN":
        raise HTTPException(status_code=403, detail="Solo ADMIN puede consultar la auditoría.")
    start, end = _audit_day_utc_bounds(audit_date)
    entries: list[AuditEntryResponse] = []

    audit_rows = db.execute(
        select(PayrollAuditLog, User.username)
        .outerjoin(User, User.id == PayrollAuditLog.user_id)
        .where(PayrollAuditLog.action_date >= start, PayrollAuditLog.action_date < end)
    ).all()
    for item, username in audit_rows:
        action = AUDIT_ACTION_LABELS.get(
            item.action_type,
            item.action_type.replace("_", " ").capitalize(),
        )
        detail = item.new_value or item.old_value
        if detail and len(detail) <= 180 and not detail.startswith("{"):
            action = f"{action}: {detail}"
        entries.append(AuditEntryResponse(
            action_date=_audit_datetime_in_chile(item.action_date),
            username=username or "Usuario eliminado",
            action=action,
        ))

    import_rows = db.execute(
        select(PayrollImport, User.username)
        .outerjoin(User, User.id == PayrollImport.imported_by)
        .where(PayrollImport.imported_at >= start, PayrollImport.imported_at < end)
    ).all()
    for item, username in import_rows:
        entries.append(AuditEntryResponse(
            action_date=_audit_datetime_in_chile(item.imported_at),
            username=username or "Usuario eliminado",
            action=f"Importó Excel {item.source_type}: {item.file_name}",
        ))

    export_rows = db.execute(
        select(PayrollExportLog, User.username)
        .outerjoin(User, User.id == PayrollExportLog.user_id)
        .where(PayrollExportLog.exported_at >= start, PayrollExportLog.exported_at < end)
    ).all()
    for item, username in export_rows:
        entries.append(AuditEntryResponse(
            action_date=_audit_datetime_in_chile(item.exported_at),
            username=username or "Usuario eliminado",
            action=f"Exportó planilla en formato {item.file_format}: {item.file_name}",
        ))
    return sorted(entries, key=lambda entry: entry.action_date, reverse=True)


@app.get("/api/audit/export")
def export_audit_entries(
    audit_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.manage")),
) -> Response:
    entries = list_audit_entries(audit_date, db, current_user)
    content = export_audit_pdf_bytes(audit_date, entries)
    file_name = f"Auditoria-{audit_date.isoformat()}.pdf"
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


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
    current_user: User = Depends(require_permission("payroll.email")),
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
    is_sheet = payload.email_type == "SHEET"
    recipient = "jose.videla@acsa-tec.cl" if is_sheet else "rrhh@unisan.cl"
    recipient_name = "José Tomás Videla" if is_sheet else "RRHH Unisan"
    file_name = export_file_name(
        settlement=settlement,
        file_format="pdf",
        cost_center=normalized_cost_center,
        role_type=normalized_role_type,
    )
    if is_sheet:
        file_name = f"Planilla-{file_name}"
    cycle_date = settlement["cycle"]["start_date"]
    month_names = (
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE",
    )
    email_body = (
        f"Respaldo de producción {settlement['employee']['employee_name']} correspondiente a "
        f"{month_names[cycle_date.month - 1]}/{cycle_date.year}"
    )
    email_subject = (
        f"Planilla de Liquidación - {settlement['employee']['employee_name']} - "
        f"{month_names[cycle_date.month - 1]}/{cycle_date.year}"
    )
    try:
        send_settlement_email(
            settings,
            recipient=recipient,
            recipient_name=recipient_name,
            pdf_content=export_sheet_pdf_bytes(settlement) if is_sheet else export_pdf_bytes(settlement),
            pdf_file_name=file_name,
            subject=email_subject,
            body=email_body,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (OSError, smtplib.SMTPException) as exc:
        raise HTTPException(
            status_code=502,
            detail="El servidor de correo rechazó o no pudo completar el envío SMTP.",
        ) from exc
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="SEND_EMAIL",
        table_name="payroll_records",
        record_id=payload.employee_id,
        new_value=f"{payload.email_type} a {recipient}",
    ))
    db.commit()
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
    current_user: User = Depends(require_permission("users.manage")),
) -> UserResponse:
    try:
        user = create_user(db, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="CREATE_USER",
        table_name="payroll_users",
        record_id=user.id,
        new_value=user.username,
    ))
    db.commit()
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


@app.patch("/api/users/{user_id}/password", response_model=UserResponse)
def reset_user_password(
    user_id: int,
    payload: UserPasswordReset,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("users.manage")),
) -> UserResponse:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    user.password_hash = hash_password(payload.password)
    db.add(PayrollAuditLog(
        user_id=_.id,
        action_type="RESET_USER_PASSWORD",
        table_name="payroll_users",
        record_id=user.id,
        new_value=user.username,
    ))
    db.commit()
    return serialize_user(user)


@app.patch("/api/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.manage")),
) -> UserResponse:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    normalized_username = payload.username.strip().lower()
    duplicate = db.scalar(
        select(User).where(User.username == normalized_username, User.id != user_id)
    )
    if duplicate is not None:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe.")

    role = db.scalar(
        select(Role).where(
            Role.role_name == payload.role_name.upper(),
            Role.active.is_(True),
        )
    )
    if role is None:
        raise HTTPException(status_code=400, detail="El rol solicitado no existe o está inactivo.")
    if user.id == current_user.id and not payload.active:
        raise HTTPException(status_code=400, detail="No puede desactivar su propio usuario.")

    user.username = normalized_username
    user.full_name = payload.full_name.strip()
    user.role = role
    user.active = payload.active
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="UPDATE_USER",
        table_name="payroll_users",
        record_id=user.id,
        new_value=user.username,
    ))
    db.commit()
    return serialize_user(user)


@app.delete("/api/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.manage")),
) -> Response:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="No puede eliminar su propio usuario.")
    try:
        db.add(PayrollAuditLog(
            user_id=current_user.id,
            action_type="DELETE_USER",
            table_name="payroll_users",
            record_id=user.id,
            old_value=user.username,
        ))
        db.delete(user)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar porque el usuario tiene movimientos históricos asociados. Puede dejarlo inactivo.",
        ) from exc
    return Response(status_code=204)


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
    db.flush()
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="CREATE_HOLIDAY",
        table_name="payroll_holidays",
        record_id=holiday.id,
        new_value=f"{holiday.holiday_date.isoformat()} - {holiday.holiday_name}",
    ))
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
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="UPDATE_HOLIDAY",
        table_name="payroll_holidays",
        record_id=holiday.id,
        new_value=f"{holiday.holiday_date.isoformat()} - {holiday.holiday_name}",
    ))
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
                cost_center=next((item.cost_center for item in matches if item.cost_center), None),
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
                cost_center=next((item.cost_center for item in matches if item.cost_center), None),
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
    cost_center = normalize_worker_cost_center(payload.cost_center)
    matches = find_related_employees_by_name(db, employee_name)
    if matches:
        for employee in matches:
            employee.contract_type = contract_type
            employee.rut = rut
            employee.email = email
            employee.cargo = cargo
            employee.cost_center = cost_center
            if not employee.first_name and not employee.paternal_surname:
                apply_employee_name_parts(employee, employee_name)
        worker = min(matches, key=lambda item: item.id)
        db.add(PayrollAuditLog(
            user_id=current_user.id,
            action_type="UPDATE_WORKER",
            table_name="payroll_employees",
            record_id=worker.id,
            new_value=employee_name,
        ))
        db.commit()
        return WorkerListItemResponse(
            id=worker.id,
            employee_name=grouped_employee_display_name(matches),
            contract_type=contract_type,
            rut=rut,
            email=email,
            cargo=cargo,
            cost_center=cost_center,
        )
    worker = Employee(
        employee_name=employee_name,
        role_type="UNASSIGNED",
        contract_type=contract_type,
        rut=rut,
        email=email,
        cargo=cargo,
        cost_center=cost_center,
    )
    apply_employee_name_parts(worker, employee_name)
    db.add(worker)
    db.flush()
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="CREATE_WORKER",
        table_name="payroll_employees",
        record_id=worker.id,
        new_value=employee_name,
    ))
    db.commit()
    db.refresh(worker)
    return WorkerListItemResponse(
        id=worker.id,
        employee_name=employee_display_name(worker),
        contract_type=worker.contract_type,
        rut=worker.rut,
        email=worker.email,
        cargo=worker.cargo,
        cost_center=worker.cost_center,
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
    cost_center = normalize_worker_cost_center(payload.cost_center)
    matches = find_related_employees_by_name(db, worker.employee_name)
    for employee in matches:
        employee.contract_type = contract_type
        employee.rut = rut
        employee.email = email
        employee.cargo = cargo
        if cost_center is not None:
            employee.cost_center = cost_center
        if not employee.first_name and not employee.paternal_surname:
            apply_employee_name_parts(employee, employee.employee_name)
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="UPDATE_WORKER",
        table_name="payroll_employees",
        record_id=worker.id,
        new_value=worker.employee_name,
    ))
    db.commit()
    return WorkerListItemResponse(
        id=worker.id,
        employee_name=grouped_employee_display_name(matches),
        contract_type=contract_type,
        rut=rut,
        email=email,
        cargo=cargo,
        cost_center=next((item.cost_center for item in matches if item.cost_center), None),
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
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="DELETE_WORKER",
        table_name="payroll_employees",
        record_id=worker.id,
        old_value=worker.employee_name,
    ))
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


def _update_settlement_statuses(
    payload: SettlementStatusUpdateRequest,
    db: Session,
    current_user: User,
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
        result = settlement_engine.update_daily_statuses(
            db,
            cycle_id=payload.cycle_id,
            employee_id=payload.employee_id,
            cost_center=normalized_cost_center,
            role_type=normalized_role_type,
            updates=[(item.work_date, item.status) for item in payload.updates],
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


@app.post("/api/liquidations/statuses", response_model=SettlementResponse)
def update_liquidation_statuses(
    payload: SettlementStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> SettlementResponse:
    payload.cost_center = None
    payload.role_type = None
    return _update_settlement_statuses(payload, db, current_user)


@app.post("/api/settlements/statuses", response_model=SettlementResponse)
def update_settlement_statuses(
    payload: SettlementStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> SettlementResponse:
    return _update_settlement_statuses(payload, db, current_user)


def serialize_ipc_adjustment(item: PayrollIpcAdjustment, db: Session) -> IpcAdjustmentResponse:
    cycle = db.get(PayrollCycle, item.effective_from_cycle_id)
    if cycle is None:
        raise HTTPException(status_code=409, detail="El ciclo del ajuste IPC no existe.")
    return IpcAdjustmentResponse(
        id=item.id,
        percentage=item.percentage,
        effective_from_cycle_id=item.effective_from_cycle_id,
        effective_from_cycle_name=cycle.cycle_name,
        status=item.status,
        created_at=item.created_at,
        updated_at=item.updated_at,
        applied_at=item.applied_at,
    )


@app.get("/api/exports/softland")
def export_softland_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.softland")),
) -> Response:
    try:
        cycle, rows, employee_ids = build_softland_rows(
            db,
            cycle_id=cycle_id,
            settlement_engine=settlement_engine,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    month_file = cycle.end_date.strftime("%m-%Y")
    file_name = f"Export Softland ({month_file}).xlsx"
    content = export_softland_xlsx_bytes(rows)
    for employee_id in employee_ids:
        log_export(
            db,
            current_user=current_user,
            cycle_id=cycle_id,
            employee_id=employee_id,
            cost_center=None,
            role_type=None,
            file_format="xlsx",
            file_name=file_name,
            export_scope_override="SOFTLAND",
        )
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@app.get("/api/rates/ipc-adjustments", response_model=list[IpcAdjustmentResponse])
def list_ipc_adjustments(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("rates.read")),
) -> list[IpcAdjustmentResponse]:
    items = db.scalars(select(PayrollIpcAdjustment).order_by(PayrollIpcAdjustment.id.desc())).all()
    return [serialize_ipc_adjustment(item, db) for item in items]


@app.post("/api/rates/ipc-adjustments", response_model=IpcAdjustmentResponse, status_code=201)
def create_ipc_adjustment(
    payload: IpcAdjustmentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rates.edit")),
) -> IpcAdjustmentResponse:
    if db.get(PayrollCycle, payload.effective_from_cycle_id) is None:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado.")
    item = PayrollIpcAdjustment(
        percentage=payload.percentage,
        effective_from_cycle_id=payload.effective_from_cycle_id,
        status="DRAFT",
        created_by=current_user.id,
    )
    db.add(item)
    db.flush()
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="CREATE_IPC_ADJUSTMENT",
        table_name="payroll_ipc_adjustments",
        record_id=item.id,
        new_value=str(item.percentage),
    ))
    db.commit()
    db.refresh(item)
    return serialize_ipc_adjustment(item, db)


@app.put("/api/rates/ipc-adjustments/{adjustment_id}", response_model=IpcAdjustmentResponse)
def update_ipc_adjustment(
    adjustment_id: int,
    payload: IpcAdjustmentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rates.edit")),
) -> IpcAdjustmentResponse:
    item = db.get(PayrollIpcAdjustment, adjustment_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Ajuste IPC no encontrado.")
    if item.status != "DRAFT":
        raise HTTPException(status_code=409, detail="Sólo se puede editar un ajuste IPC pendiente.")
    item.percentage = payload.percentage
    if db.get(PayrollCycle, payload.effective_from_cycle_id) is None:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado.")
    item.effective_from_cycle_id = payload.effective_from_cycle_id
    item.updated_at = datetime.utcnow()
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="UPDATE_IPC_ADJUSTMENT",
        table_name="payroll_ipc_adjustments",
        record_id=item.id,
        new_value=str(item.percentage),
    ))
    db.commit()
    db.refresh(item)
    return serialize_ipc_adjustment(item, db)


def _rate_snapshot(db: Session) -> dict[str, dict[str, object]]:
    return {
        str(rate.id): {
            "amount": str(rate.amount),
            "contract_type": rate.contract_type,
            "effective_from_cycle_id": rate.effective_from_cycle_id,
            "effective_to_cycle_id": rate.effective_to_cycle_id,
            "active": rate.active,
        }
        for rate in db.scalars(select(PayrollConceptRate).order_by(PayrollConceptRate.id)).all()
    }


def _restore_rate_snapshot(db: Session, snapshot: dict[str, dict[str, object]], now: datetime) -> None:
    current_rates = {
        rate.id: rate for rate in db.scalars(select(PayrollConceptRate)).all()
    }
    snapshot_ids = {int(rate_id) for rate_id in snapshot}
    for rate_id, rate in current_rates.items():
        if rate_id not in snapshot_ids:
            rate.active = False
            rate.updated_at = now
    for rate_id, values in snapshot.items():
        rate = current_rates.get(int(rate_id))
        if rate is None:
            continue
        rate.amount = Decimal(str(values["amount"]))
        rate.contract_type = values.get("contract_type")
        rate.effective_from_cycle_id = values.get("effective_from_cycle_id")
        rate.effective_to_cycle_id = values.get("effective_to_cycle_id")
        rate.active = bool(values.get("active"))
        rate.updated_at = now


@app.post("/api/rates/ipc-adjustments/{adjustment_id}/apply", response_model=IpcAdjustmentResponse)
def apply_ipc_adjustment(
    adjustment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rates.edit")),
) -> IpcAdjustmentResponse:
    item = db.get(PayrollIpcAdjustment, adjustment_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Ajuste IPC no encontrado.")
    now = datetime.utcnow()
    is_initial_application = item.status == "DRAFT"
    if item.status == "DRAFT":
        target_cycle = db.get(PayrollCycle, item.effective_from_cycle_id)
        if target_cycle is None:
            raise HTTPException(status_code=404, detail="Ciclo no encontrado.")
        item.snapshot_before = json.dumps(_rate_snapshot(db))
        active_rates = list(
            db.scalars(
                select(PayrollConceptRate)
                .where(PayrollConceptRate.active.is_(True))
                .order_by(PayrollConceptRate.id)
            ).all()
        )
        pairs = sorted(
            {(rate.concept_id, rate.contract_type) for rate in active_rates},
            key=lambda pair: (pair[0], pair[1] or ""),
        )
        factor = Decimal("1") + (item.percentage / Decimal("100"))
        effective_rate_ids: set[int] = set()
        for concept_id, contract_type in pairs:
            effective = concept_rate_service.effective_rates(
                db,
                concept_ids=[concept_id],
                cycle_id=target_cycle.id,
                contract_type=contract_type,
            ).get(concept_id)
            if effective is None or effective.contract_type != contract_type:
                continue
            if effective.id in effective_rate_ids:
                continue
            effective_rate_ids.add(effective.id)
            new_amount = (effective.amount * factor).quantize(
                Decimal("0.0001"), rounding=ROUND_HALF_UP
            )
            concept_rate_service.save_rate(
                db,
                concept_id=concept_id,
                cycle_id=target_cycle.id,
                amount=new_amount,
                apply_mode="FROM_CYCLE_FORWARD",
                contract_type=contract_type,
                admin=current_user,
            )
        db.flush()
        item.snapshot_after = json.dumps(_rate_snapshot(db))
        item.status = "APPLIED"
        item.applied_at = now
    else:
        snapshot = json.loads(item.snapshot_after or "{}")
        _restore_rate_snapshot(db, snapshot, now)
    item.updated_at = now
    db.add(PayrollAuditLog(
        user_id=current_user.id,
        action_type="APPLY_IPC_ADJUSTMENT" if is_initial_application else "RESTORE_IPC_ADJUSTMENT",
        table_name="payroll_ipc_adjustments",
        record_id=item.id,
        field_name="percentage",
        old_value=None,
        new_value=str(item.percentage),
    ))
    db.commit()
    db.refresh(item)
    return serialize_ipc_adjustment(item, db)


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


@app.get("/api/settlements/activities", response_model=list[RateListItemResponse])
def list_settlement_activities(
    cost_center: str,
    role_type: str,
    cycle_id: int,
    contract_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.edit")),
) -> list[RateListItemResponse]:
    return list_rates(
        cost_center=cost_center,
        role_type=role_type,
        cycle_id=cycle_id,
        contract_type=contract_type,
        db=db,
        _=current_user,
    )


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
        select(PayrollImport, User.username, PayrollCycle.cycle_name)
        .join(User, User.id == PayrollImport.imported_by)
        .join(PayrollCycle, PayrollCycle.id == PayrollImport.cycle_id)
        .order_by(PayrollImport.imported_at.desc())
        .limit(100)
    ).all()
    return [
        ImportHistoryResponse(
            id=payroll_import.id,
            cycle_id=payroll_import.cycle_id,
            cycle_name=cycle_name,
            imported_at=payroll_import.imported_at,
            file_name=payroll_import.file_name,
            source_type=payroll_import.source_type,
            rows_imported=payroll_import.rows_imported,
            imported_by=username,
        )
        for payroll_import, username, cycle_name in rows
    ]


@app.delete(
    "/api/imports/cycles/{cycle_id}/{source_type}",
    response_model=ImportCycleDeleteResponse,
)
def delete_imported_cycle(
    cycle_id: int,
    source_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payroll.import")),
) -> ImportCycleDeleteResponse:
    if current_user.role.role_name != "ADMIN":
        raise HTTPException(status_code=403, detail="Solo ADMIN puede eliminar ciclos importados.")
    normalized_source = source_type.upper()
    if normalized_source not in {"DR", "SERVICES"}:
        raise HTTPException(status_code=400, detail="Tipo de importación inválido.")
    cycle = db.get(PayrollCycle, cycle_id)
    if cycle is None:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado.")
    import_ids = list(
        db.scalars(
            select(PayrollImport.id).where(
                PayrollImport.cycle_id == cycle_id,
                PayrollImport.source_type == normalized_source,
            )
        ).all()
    )
    if not import_ids:
        raise HTTPException(
            status_code=404,
            detail="No existe una importación de ese tipo para el ciclo seleccionado.",
        )
    try:
        records_deleted = db.execute(
            delete(PayrollRecord).where(PayrollRecord.import_id.in_(import_ids))
        ).rowcount or 0
        overrides_deleted = db.execute(
            delete(PayrollCellOverride).where(
                PayrollCellOverride.cycle_id == cycle_id,
                PayrollCellOverride.cost_center == normalized_source,
            )
        ).rowcount or 0
        adjustments_deleted = db.execute(
            delete(PayrollManualAdjustment).where(
                PayrollManualAdjustment.cycle_id == cycle_id,
                PayrollManualAdjustment.cost_center == normalized_source,
            )
        ).rowcount or 0
        db.execute(
            delete(PayrollExportLog).where(
                PayrollExportLog.cycle_id == cycle_id,
                PayrollExportLog.cost_center == normalized_source,
            )
        )
        imports_deleted = db.execute(
            delete(PayrollImport).where(PayrollImport.id.in_(import_ids))
        ).rowcount or 0
        db.add(
            PayrollAuditLog(
                user_id=current_user.id,
                action_type="DELETE_IMPORTED_CYCLE",
                table_name="payroll_imports",
                record_id=cycle_id,
                field_name="source_type",
                old_value=f"{cycle.cycle_name} / {normalized_source}",
                new_value=json.dumps(
                    {
                        "imports_deleted": imports_deleted,
                        "records_deleted": records_deleted,
                        "overrides_deleted": overrides_deleted,
                        "adjustments_deleted": adjustments_deleted,
                    }
                ),
            )
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    return ImportCycleDeleteResponse(
        cycle_id=cycle_id,
        cycle_name=cycle.cycle_name,
        source_type=normalized_source,
        imports_deleted=imports_deleted,
        records_deleted=records_deleted,
        overrides_deleted=overrides_deleted,
        adjustments_deleted=adjustments_deleted,
    )


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
