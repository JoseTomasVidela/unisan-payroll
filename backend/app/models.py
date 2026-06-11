from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


role_permissions = Table(
    "payroll_role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("payroll_roles.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "permission_id",
        ForeignKey("payroll_permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Permission(Base):
    __tablename__ = "payroll_permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    permission_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))

    roles: Mapped[list["Role"]] = relationship(
        secondary=role_permissions,
        back_populates="permissions",
    )


class Role(Base):
    __tablename__ = "payroll_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    permissions: Mapped[list[Permission]] = relationship(
        secondary=role_permissions,
        back_populates="roles",
        lazy="selectin",
    )
    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "payroll_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    password_hash: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(ForeignKey("payroll_roles.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    role: Mapped[Role] = relationship(back_populates="users", lazy="selectin")


class PayrollCycle(Base):
    __tablename__ = "payroll_cycles"

    id: Mapped[int] = mapped_column(primary_key=True)
    cycle_name: Mapped[str] = mapped_column(String(120))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)


class Employee(Base):
    __tablename__ = "payroll_employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_name: Mapped[str] = mapped_column(String(180), index=True)
    role_type: Mapped[str] = mapped_column(String(32), index=True)
    contract_type: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)


class PayrollImport(Base):
    __tablename__ = "payroll_imports"

    id: Mapped[int] = mapped_column(primary_key=True)
    cycle_id: Mapped[int] = mapped_column(ForeignKey("payroll_cycles.id"))
    source_type: Mapped[str] = mapped_column(String(32))
    cost_center: Mapped[str] = mapped_column(String(32))
    file_name: Mapped[str] = mapped_column(String(255))
    imported_by: Mapped[int] = mapped_column(ForeignKey("payroll_users.id"))
    rows_imported: Mapped[int] = mapped_column(Integer, default=0)
    imported_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PayrollRecord(Base):
    __tablename__ = "payroll_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    cycle_id: Mapped[int] = mapped_column(ForeignKey("payroll_cycles.id"), index=True)
    import_id: Mapped[int] = mapped_column(ForeignKey("payroll_imports.id"), index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("payroll_employees.id"), index=True)
    source_type: Mapped[str] = mapped_column(String(32), index=True)
    cost_center: Mapped[str] = mapped_column(String(32), index=True)
    role_type: Mapped[str] = mapped_column(String(32), index=True)
    source_employee_name: Mapped[str] = mapped_column(String(180), index=True)
    source_employee_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_row_number: Mapped[int] = mapped_column(Integer)
    source_row_hash: Mapped[str] = mapped_column(String(64), index=True)
    source_person_slot: Mapped[str] = mapped_column(String(32), index=True)
    work_date: Mapped[date] = mapped_column(Date, index=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str | None] = mapped_column(String(120), nullable=True)

    dispatch_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    entry_before_1930_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    entry_before_0730_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    exit_after_1930_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    fair_week_1_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    fair_week_2_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    outside_radius_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    outside_radius_v_region_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    saturday_week_1_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    sunday_week_1_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    saturday_week_2_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    sunday_week_2_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    client_trips_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    saturday_after_1600_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    sunday_after_1600_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    cleaning_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    drying_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    weekend_cleaning_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    weekend_drying_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    event_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    water_point_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    kit_delivery_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    lavatory_load_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    large_trash_bin_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    small_trash_bin_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    fosa_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    riles_suction_flag: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)


class PayrollConcept(Base):
    __tablename__ = "payroll_concepts"

    id: Mapped[int] = mapped_column(primary_key=True)
    concept_code: Mapped[str] = mapped_column(String(50))
    concept_name: Mapped[str] = mapped_column(String(200))
    db_field: Mapped[str] = mapped_column(String(64))
    source_type: Mapped[str] = mapped_column(String(32))
    cost_center: Mapped[str] = mapped_column(String(32), index=True)
    role_type: Mapped[str] = mapped_column(String(32), index=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PayrollConceptRate(Base):
    __tablename__ = "payroll_concept_rates"

    id: Mapped[int] = mapped_column(primary_key=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("payroll_concepts.id"), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    contract_type: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)
    effective_from_cycle_id: Mapped[int | None] = mapped_column(
        ForeignKey("payroll_cycles.id"), nullable=True, index=True
    )
    effective_to_cycle_id: Mapped[int | None] = mapped_column(
        ForeignKey("payroll_cycles.id"), nullable=True, index=True
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("payroll_users.id"), nullable=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PayrollManualAdjustment(Base):
    __tablename__ = "payroll_manual_adjustments"

    id: Mapped[int] = mapped_column(primary_key=True)
    cycle_id: Mapped[int] = mapped_column(ForeignKey("payroll_cycles.id"), index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("payroll_employees.id"), index=True)
    cost_center: Mapped[str] = mapped_column(String(32), index=True)
    role_type: Mapped[str] = mapped_column(String(32), index=True)
    adjustment_type: Mapped[str] = mapped_column(String(40), index=True)
    adjustment_name: Mapped[str] = mapped_column(String(200))
    adjustment_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    units: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("payroll_users.id"), nullable=True
    )
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("payroll_users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PayrollCellOverride(Base):
    __tablename__ = "payroll_cell_overrides"

    id: Mapped[int] = mapped_column(primary_key=True)
    cycle_id: Mapped[int] = mapped_column(ForeignKey("payroll_cycles.id"), index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("payroll_employees.id"), index=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("payroll_concepts.id"), index=True)
    cost_center: Mapped[str] = mapped_column(String(32), index=True)
    role_type: Mapped[str] = mapped_column(String(32), index=True)
    work_date: Mapped[date] = mapped_column(Date, index=True)
    override_value: Mapped[Decimal] = mapped_column(Numeric(14, 4), default=0)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("payroll_users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PayrollAuditLog(Base):
    __tablename__ = "payroll_audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("payroll_users.id"), nullable=True)
    action_type: Mapped[str] = mapped_column(String(50))
    table_name: Mapped[str] = mapped_column(String(100))
    record_id: Mapped[int] = mapped_column(Integer)
    field_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    old_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    action_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PayrollExportLog(Base):
    __tablename__ = "payroll_export_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("payroll_users.id"), nullable=True)
    export_scope: Mapped[str] = mapped_column(String(32))
    file_format: Mapped[str] = mapped_column(String(16))
    cycle_id: Mapped[int] = mapped_column(ForeignKey("payroll_cycles.id"), index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("payroll_employees.id"), index=True)
    cost_center: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    role_type: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    file_name: Mapped[str] = mapped_column(String(255))
    exported_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
