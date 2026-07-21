from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .security import validate_password


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=256)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    role: str
    permissions: list[str]
    active: bool


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    full_name: str = Field(min_length=1, max_length=160)
    password: str = Field(min_length=6, max_length=256)
    role_name: str
    active: bool = True

    @field_validator("password")
    @classmethod
    def password_policy(cls, value: str) -> str:
        return validate_password(value)


class UserActiveUpdate(BaseModel):
    active: bool


class SettlementEmailRequest(BaseModel):
    cycle_id: int
    employee_id: int
    cost_center: str | None = None
    role_type: str | None = None


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    permission_code: str
    description: str


class RoleResponse(BaseModel):
    role_name: str
    description: str
    active: bool
    permissions: list[str]


class CycleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cycle_name: str
    start_date: date
    end_date: date


class ImportHistoryResponse(BaseModel):
    id: int
    imported_at: datetime
    file_name: str
    source_type: str
    rows_imported: int
    imported_by: str


class ImportResponse(BaseModel):
    import_ids: list[int]
    file_name: str
    source_type: str
    cycle_ids: list[int]
    cycles_created: int
    rows_read: int
    records_inserted: int
    workers_created: int
    rows_outside_cycle: int
    errors: list[str]
    possible_reimports_confirmed: int


class SearchResponse(BaseModel):
    cycle_ids: list[int]
    records_count: int


class SearchEmployeeOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_name: str
    contract_type: str | None = None
    rut: str | None = None
    email: str | None = None
    cargo: str | None = None


class EmployeeOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_name: str
    contract_type: str | None = None
    rut: str | None = None
    email: str | None = None
    cargo: str | None = None


class WorkerListItemResponse(BaseModel):
    id: int
    employee_name: str
    contract_type: str | None
    rut: str | None
    email: str | None
    cargo: str | None


class WorkerCreateRequest(BaseModel):
    employee_name: str = Field(min_length=1, max_length=180)
    contract_type: str | None = Field(default=None, pattern="^(NEW|OLD)?$")
    rut: str | None = Field(default=None, max_length=32)
    email: str | None = Field(default=None, max_length=255)
    cargo: str | None = Field(default=None, max_length=180)


class WorkerUpdateRequest(BaseModel):
    contract_type: str | None = Field(default=None, pattern="^(NEW|OLD)?$")
    rut: str | None = Field(default=None, max_length=32)
    email: str | None = Field(default=None, max_length=255)
    cargo: str | None = Field(default=None, max_length=180)


class SettlementDateResponse(BaseModel):
    date: date
    label: str
    weekday: str
    is_holiday: bool = False
    holiday_names: list[str] = []


class SettlementStatusResponse(BaseModel):
    date: date
    status: str | None


class SettlementDailyValueResponse(BaseModel):
    date: date
    value: Decimal | None
    editable: bool


class SettlementRowResponse(BaseModel):
    row_type: str
    concept_id: int | None
    rate_id: int | None
    concept_code: str
    concept_name: str
    db_field: str | None
    units: Decimal | None
    rate: Decimal | None
    total: Decimal | None
    editable: bool
    daily_values: list[SettlementDailyValueResponse]


class SettlementDailyTotalResponse(BaseModel):
    date: date
    value: Decimal


class SettlementEmployeeResponse(BaseModel):
    id: int
    employee_name: str
    contract_type: str | None = None
    rut: str | None = None
    email: str | None = None
    cargo: str | None = None


class SettlementResponse(BaseModel):
    employee: SettlementEmployeeResponse
    cycle: CycleResponse
    cost_center: str | None
    role_type: str | None
    dates: list[SettlementDateResponse]
    statuses: list[SettlementStatusResponse]
    rows: list[SettlementRowResponse]
    daily_totals: list[SettlementDailyTotalResponse]
    total_to_pay: Decimal
    week_corrida: Decimal
    production_total: Decimal


class HolidayResponse(BaseModel):
    id: int | None = None
    holiday_date: date
    holiday_name: str
    holiday_scope: str
    active: bool
    is_default: bool
    editable: bool


class HolidayCreateRequest(BaseModel):
    holiday_date: date
    holiday_name: str = Field(min_length=1, max_length=200)
    holiday_scope: str = Field(pattern="^(CHILE|WORLD|CUSTOM)$")
    active: bool = True


class HolidayUpdateRequest(BaseModel):
    holiday_date: date
    holiday_name: str = Field(min_length=1, max_length=200)
    holiday_scope: str = Field(pattern="^(CHILE|WORLD|CUSTOM)$")
    active: bool = True


class ManualAdjustmentAuditResponse(BaseModel):
    id: int
    action_type: str
    old_value: str | None
    new_value: str | None
    action_date: datetime
    user_name: str | None


class ManualAdjustmentResponse(BaseModel):
    id: int
    cycle_id: int
    employee_id: int
    cost_center: str
    role_type: str
    adjustment_type: str
    description: str | None
    units: Decimal | None
    amount: Decimal
    observations: str | None
    active: bool
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None
    history: list[ManualAdjustmentAuditResponse] = []


class ManualAdjustmentCreateRequest(BaseModel):
    cycle_id: int
    employee_id: int
    adjustment_type: str = Field(
        pattern="^(VACATION|BONUS|MANUAL_ADJUSTMENT)$"
    )
    description: str | None = Field(default=None, max_length=200)
    units: Decimal | None = Field(default=None, ge=0, max_digits=14, decimal_places=4)
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=4)
    observations: str | None = Field(default=None, max_length=4000)


class ManualAdjustmentUpdateRequest(BaseModel):
    adjustment_type: str = Field(
        pattern="^(VACATION|BONUS|MANUAL_ADJUSTMENT)$"
    )
    description: str | None = Field(default=None, max_length=200)
    units: Decimal | None = Field(default=None, ge=0, max_digits=14, decimal_places=4)
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=4)
    observations: str | None = Field(default=None, max_length=4000)


class ConceptRateUpdate(BaseModel):
    concept_id: int
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=4)
    apply_mode: str = Field(pattern="^(SINGLE_CYCLE|FROM_CYCLE_FORWARD)$")


class SettlementRateUpdateRequest(BaseModel):
    cycle_id: int
    employee_id: int
    cost_center: str
    role_type: str
    updates: list[ConceptRateUpdate] = Field(min_length=1)


class SettlementCellUpdateItem(BaseModel):
    concept_id: int
    work_date: date
    value: Decimal = Field(ge=0, max_digits=14, decimal_places=4)


class SettlementCellUpdateRequest(BaseModel):
    cycle_id: int
    employee_id: int
    cost_center: str | None = None
    role_type: str | None = None
    updates: list[SettlementCellUpdateItem] = Field(min_length=1)


class RateListItemResponse(BaseModel):
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


class RateCreateRequest(BaseModel):
    concept_id: int
    cycle_id: int
    contract_type: str | None = Field(default=None, pattern="^(NEW|OLD)?$")
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=4)
    apply_mode: str = Field(pattern="^(SINGLE_CYCLE|FROM_CYCLE_FORWARD)$")


class RateUpdateRequest(BaseModel):
    cycle_id: int
    contract_type: str | None = Field(default=None, pattern="^(NEW|OLD)?$")
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=4)
    apply_mode: str = Field(pattern="^(SINGLE_CYCLE|FROM_CYCLE_FORWARD)$")


class ReimportWarningResponse(BaseModel):
    requires_confirmation: bool = True
    message: str
    possible_reimports: int
    rows_read: int
    records_ready: int
    rows_outside_cycle: int
    errors: list[str]
