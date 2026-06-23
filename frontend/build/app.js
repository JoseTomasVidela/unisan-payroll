const loginScreen = document.getElementById("login-screen");
const appShell = document.getElementById("app-shell");
const loginBtn = document.getElementById("login-btn");
const logoutBtn = document.getElementById("logout-btn");
const toggleSidebar = document.getElementById("toggle-sidebar");

const views = document.querySelectorAll(".view");
const navItems = document.querySelectorAll(".nav-item[data-view]");
const title = document.getElementById("page-title");
const breadcrumb = document.getElementById("breadcrumb");
const liquidationView = document.getElementById("liquidation-view");
const liquidationPanelTitle = document.getElementById("liquidation-panel-title");
const spreadsheet = document.getElementById("spreadsheet");
const spreadsheetSearch = document.getElementById("spreadsheet-search");
const editBtn = document.getElementById("edit-btn");
const saveBtn = document.getElementById("save-btn");
const cancelEditBtn = document.getElementById("cancel-edit-btn");
const modal = document.getElementById("confirm-modal");
const cancelSave = document.getElementById("cancel-save");
const confirmSave = document.getElementById("confirm-save");
const newUserBtn = document.getElementById("new-user-btn");
const cancelUserBtn = document.getElementById("cancel-user-btn");
const userForm = document.getElementById("user-form");
const usersNav = document.getElementById("users-nav");
const usersTableBody = document.getElementById("users-table-body");
const saveUserBtn = document.getElementById("save-user-btn");
const userFullName = document.getElementById("user-full-name");
const userUsername = document.getElementById("user-username");
const userPassword = document.getElementById("user-password");
const userRole = document.getElementById("user-role");
const userActive = document.getElementById("user-active");
const loginUsername = document.getElementById("login-username");
const loginPassword = document.getElementById("login-password");
const loginRemember = document.getElementById("login-remember");
const loginShowPassword = document.getElementById("login-show-password");
const drImportFile = document.getElementById("dr-import-file");
const drImportBtn = document.getElementById("dr-import-btn");
const drImportSelected = document.getElementById("dr-import-selected");
const drImportCard = drImportFile.closest(".upload-card");
const servicesImportFile = document.getElementById("services-import-file");
const servicesImportBtn = document.getElementById("services-import-btn");
const servicesImportSelected = document.getElementById("services-import-selected");
const servicesImportCard = servicesImportFile.closest(".upload-card");
const importsTableBody = document.getElementById("imports-table-body");
const holidayCalendar = document.getElementById("holiday-calendar");
const holidayMonthLabel = document.getElementById("holiday-month-label");
const holidayPrevMonthBtn = document.getElementById("holiday-prev-month-btn");
const holidayNextMonthBtn = document.getElementById("holiday-next-month-btn");
const holidayNewBtn = document.getElementById("holiday-new-btn");
const liquidationCycle = document.getElementById("liquidation-cycle");
const liquidationEmployee = document.getElementById("liquidation-employee");
const settlementEmployeeName = document.getElementById("settlement-employee-name");
const settlementCycleName = document.getElementById("settlement-cycle-name");
const searchCycle = document.getElementById("search-cycle");
const searchEmployee = document.getElementById("search-employee");
const searchCycleSummary = document.getElementById("search-cycle-summary");
const searchEmployeeSummary = document.getElementById("search-employee-summary");
const searchBtn = document.getElementById("search-btn");
const searchEditBtn = document.getElementById("search-edit-btn");
const searchAdjustmentsBtn = document.getElementById("search-adjustments-btn");
const searchSaveBtn = document.getElementById("search-save-btn");
const searchCancelEditBtn = document.getElementById("search-cancel-edit-btn");
const searchExportExcelBtn = document.getElementById("search-export-excel-btn");
const searchExportPdfBtn = document.getElementById("search-export-pdf-btn");
const searchEmailBtn = document.getElementById("search-email-btn");
const searchSoftlandBtn = document.getElementById("search-softland-btn");
const searchResultTitle = document.getElementById("search-result-title");
const searchSettlementEmployeeName = document.getElementById("search-settlement-employee-name");
const searchSettlementCycleName = document.getElementById("search-settlement-cycle-name");
const searchSettlementCenter = document.getElementById("search-settlement-center");
const searchSettlementRole = document.getElementById("search-settlement-role");
const searchSingleActions = document.getElementById("search-single-actions");
const searchSingleEditBtn = document.getElementById("search-single-edit-btn");
const searchSingleAdjustmentsBtn = document.getElementById("search-single-adjustments-btn");
const liquidationExportExcelBtn = document.getElementById("liquidation-export-excel-btn");
const liquidationExportPdfBtn = document.getElementById("liquidation-export-pdf-btn");
const liquidationEmailBtn = document.getElementById("liquidation-email-btn");
const liquidationSoftlandBtn = document.getElementById("liquidation-softland-btn");
const ratesCycle = document.getElementById("rates-cycle");
const ratesTableBody = document.getElementById("rates-table-body");
const ratesTabs = document.getElementById("rates-tabs");
const rateModal = document.getElementById("rate-modal");
const rateModalConcept = document.getElementById("rate-modal-concept");
const rateModalCurrent = document.getElementById("rate-modal-current");
const rateModalAmount = document.getElementById("rate-modal-amount");
const rateModalCycle = document.getElementById("rate-modal-cycle");
const rateCancelBtn = document.getElementById("rate-cancel-btn");
const rateSaveBtn = document.getElementById("rate-save-btn");
const workersTableBody = document.getElementById("workers-table-body");
const newWorkerBtn = document.getElementById("new-worker-btn");
const workerModal = document.getElementById("worker-modal");
const workerName = document.getElementById("worker-name");
const workerContract = document.getElementById("worker-contract");
const workerRut = document.getElementById("worker-rut");
const workerEmail = document.getElementById("worker-email");
const workerCargo = document.getElementById("worker-cargo");
const saveWorkerBtn = document.getElementById("save-worker-btn");
const cancelWorkerBtn = document.getElementById("cancel-worker-btn");
const adjustmentsModal = document.getElementById("adjustments-modal");
const adjustmentWorker = document.getElementById("adjustment-worker");
const adjustmentCycle = document.getElementById("adjustment-cycle");
const adjustmentType = document.getElementById("adjustment-type");
const adjustmentUnits = document.getElementById("adjustment-units");
const adjustmentAmount = document.getElementById("adjustment-amount");
const adjustmentObservations = document.getElementById("adjustment-observations");
const adjustmentNewBtn = document.getElementById("adjustment-new-btn");
const adjustmentSaveBtn = document.getElementById("adjustment-save-btn");
const adjustmentDeleteBtn = document.getElementById("adjustment-delete-btn");
const adjustmentCloseBtn = document.getElementById("adjustment-close-btn");
const adjustmentsTableBody = document.getElementById("adjustments-table-body");
const searchEditModal = document.getElementById("search-edit-modal");
const searchEditEmployeeName = document.getElementById("search-edit-employee-name");
const searchEditCycleName = document.getElementById("search-edit-cycle-name");
const searchEditSpreadsheet = document.getElementById("search-edit-spreadsheet");
const searchEditModalCancelBtn = document.getElementById("search-edit-modal-cancel-btn");
const searchEditModalSaveBtn = document.getElementById("search-edit-modal-save-btn");
const holidayModal = document.getElementById("holiday-modal");
const holidayDateInput = document.getElementById("holiday-date");
const holidayNameInput = document.getElementById("holiday-name");
const holidayActiveInput = document.getElementById("holiday-active");
const holidayCancelBtn = document.getElementById("holiday-cancel-btn");
const holidaySaveBtn = document.getElementById("holiday-save-btn");
const statusModal = document.getElementById("status-modal");
const statusSpinner = document.getElementById("status-spinner");
const statusTitle = document.getElementById("status-title");
const statusMessage = document.getElementById("status-message");
const statusCloseBtn = document.getElementById("status-close-btn");

let editMode = false;
let currentUser = null;
let currentContext = null;
let currentView = "search";
let currentRatesContext = "dr-driver-old";
let cyclesCache = [];
let currentRateRow = null;
let editingWorkerId = null;
let activeSheetMode = "context";
let activeSheetContainer = spreadsheet;
let activeSheetEmployeeName = settlementEmployeeName;
let activeSheetCycleName = settlementCycleName;
let activeSheetContext = null;
let manualAdjustments = [];
let selectedAdjustmentId = null;
let contextEmployeesCache = [];
let holidayMonthCursor = new Date();
holidayMonthCursor = new Date(holidayMonthCursor.getFullYear(), holidayMonthCursor.getMonth(), 1);
let holidayEntries = [];
let editingHolidayId = null;
const configuredApiBaseUrl = window.__PAYROLL_CONFIG__?.apiBaseUrl?.trim();
const defaultApiBaseUrl = ["127.0.0.1", "localhost"].includes(window.location.hostname)
    ? "http://127.0.0.1:8010/api"
    : `${window.location.origin}/payroll/api`;
const apiBaseUrl = (configuredApiBaseUrl || defaultApiBaseUrl).replace(/\/$/, "");
const rememberedUsernameKey = "payroll_remembered_username";

const adjustmentTypeLabels = {
    VACATION: "Vacaciones",
    BONUS: "Bono",
    MANUAL_ADJUSTMENT: "Ajuste manual"
};


function hasPermission(permission) {
    return currentUser?.permissions.includes(permission);
}

function escapeHtml(value) {
    const element = document.createElement("div");
    element.textContent = String(value);
    return element.innerHTML;
}

function adjustmentTypeLabel(value) {
    return adjustmentTypeLabels[value] || value || "";
}

function formatStatusLabel(value) {
    if (!value) return "";
    const labels = {
        "libre compensatorio": "Libre Comp.",
        "sin produccion": "Sin Prod.",
        "sin producción": "Sin Prod.",
        "inasistencia": "Inasis.",
        "vacaciones": "Vac.",
        "descanso": "Desc.",
        "feriado": "Feriado",
        "licencia": "Licencia"
    };
    return String(value)
        .split("/")
        .map(part => part.trim())
        .filter(Boolean)
        .map(part => labels[part.toLowerCase()] || part)
        .join(" / ");
}

function toIsoDate(localDate) {
    const year = localDate.getFullYear();
    const month = String(localDate.getMonth() + 1).padStart(2, "0");
    const day = String(localDate.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

function parseIsoDate(value) {
    const [year, month, day] = String(value).split("-").map(Number);
    return new Date(year, month - 1, day);
}

function updateImportSelection(fileInput, button, selectedLabel, buttonLabel, card, imported = false, fileName = "") {
    const file = fileInput.files[0];
    const visibleName = fileName || file?.name || "";
    const hasFile = Boolean(visibleName);
    button.disabled = !file;
    selectedLabel.textContent = imported
        ? `${visibleName} importado correctamente`
        : hasFile
            ? visibleName
            : "Formato permitido: .xlsx";
    button.textContent = buttonLabel;
    card?.classList.toggle("has-file", hasFile && !imported);
    card?.classList.toggle("is-imported", imported);
}

async function apiRequest(path, options = {}) {
    const token = localStorage.getItem("payroll_access_token");
    const isFormData = options.body instanceof FormData;
    const response = await fetch(`${apiBaseUrl}${path}`, {
        ...options,
        headers: {
            ...(!isFormData ? { "Content-Type": "application/json" } : {}),
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...options.headers
        }
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        let detailMessage = "No fue posible completar la solicitud.";
        if (Array.isArray(data.detail)) {
            detailMessage = data.detail
                .map(item => item?.msg || item?.message || "Dato invalido.")
                .join(" ");
        } else if (typeof data.detail === "string") {
            detailMessage = data.detail;
        }
        const error = new Error(
            detailMessage
        );
        error.detail = data.detail;
        throw error;
    }
    return data;
}

async function downloadApiFile(path) {
    const token = localStorage.getItem("payroll_access_token");
    const response = await fetch(`${apiBaseUrl}${path}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    if (!response.ok) {
        let detail = "No fue posible completar la solicitud.";
        try {
            const data = await response.json();
            if (typeof data.detail === "string") detail = data.detail;
        } catch (_) {
            // noop
        }
        throw new Error(detail);
    }
    const blob = await response.blob();
    const disposition = response.headers.get("Content-Disposition") || "";
    const utfMatch = disposition.match(/filename\*=UTF-8''([^;]+)/i);
    const basicMatch = disposition.match(/filename=\"([^\"]+)\"/i);
    const fileName = utfMatch
        ? decodeURIComponent(utfMatch[1])
        : basicMatch
            ? basicMatch[1]
            : "exportacion";
    const objectUrl = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(objectUrl);
}

function pendingFeature(message) {
    alert(message);
}

function showStatusModal({ title, message, loading = false, closable = false } = {}) {
    statusTitle.textContent = title || "Procesando";
    statusMessage.textContent = message || "";
    statusSpinner.classList.toggle("hidden", !loading);
    statusCloseBtn.classList.toggle("hidden", !closable);
    statusModal.classList.remove("hidden");
}

function hideStatusModal() {
    statusModal.classList.add("hidden");
}

function openPrintPreview(titleText, htmlContent) {
    const printWindow = window.open("", "_blank", "width=1280,height=900");
    if (!printWindow) {
        alert("No fue posible abrir la vista de impresion.");
        return;
    }
    printWindow.document.open();
    printWindow.document.write(`<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <title>${escapeHtml(titleText)}</title>
    <style>
        body { font-family: "Segoe UI", Arial, sans-serif; margin: 24px; color: #22313f; }
        h1 { margin: 0 0 20px; font-size: 24px; }
        h2, h3 { margin: 0 0 12px; }
        .stack-cycle-group { margin-bottom: 28px; }
        .stack-settlement-card { margin-bottom: 24px; page-break-inside: avoid; }
        .settlement-meta { display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 12px; font-size: 14px; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; }
        th, td { border: 1px solid #cfd6dc; padding: 6px 8px; text-align: center; white-space: nowrap; }
        th:first-child, td:first-child { text-align: left; }
        th:nth-child(2), td:nth-child(2), th:nth-child(3), td:nth-child(3), th:nth-child(4), td:nth-child(4) { min-width: 70px; }
    </style>
</head>
<body>
    <h1>${escapeHtml(titleText)}</h1>
    ${htmlContent}
</body>
</html>`);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
}

function resetHolidayForm() {
    editingHolidayId = null;
    holidayDateInput.value = toIsoDate(new Date());
    holidayNameInput.value = "";
    holidayActiveInput.checked = true;
}

function closeHolidayModal() {
    holidayModal.classList.add("hidden");
    resetHolidayForm();
}

function openHolidayModal({
    id = null,
    holiday_date = toIsoDate(new Date()),
    holiday_name = "",
    active = true
} = {}) {
    editingHolidayId = id;
    holidayDateInput.value = holiday_date;
    holidayNameInput.value = holiday_name;
    holidayActiveInput.checked = Boolean(active);
    holidayModal.classList.remove("hidden");
}

function holidaysByDate() {
    return holidayEntries.reduce((map, item) => {
        if (!item.active) return map;
        const list = map.get(item.holiday_date) || [];
        list.push(item);
        map.set(item.holiday_date, list);
        return map;
    }, new Map());
}

function renderHolidayCalendar() {
    const firstDay = new Date(holidayMonthCursor.getFullYear(), holidayMonthCursor.getMonth(), 1);
    const lastDay = new Date(holidayMonthCursor.getFullYear(), holidayMonthCursor.getMonth() + 1, 0);
    const startOffset = (firstDay.getDay() + 6) % 7;
    const activeByDate = holidaysByDate();
    const todayIso = toIsoDate(new Date());
    const weekdayLabels = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"];
    const cells = [];
    for (let index = 0; index < startOffset; index += 1) {
        cells.push('<div class="holiday-day empty"></div>');
    }
    for (let day = 1; day <= lastDay.getDate(); day += 1) {
        const current = new Date(holidayMonthCursor.getFullYear(), holidayMonthCursor.getMonth(), day);
        const iso = toIsoDate(current);
        const items = activeByDate.get(iso) || [];
        const holidayTitle = items.length ? ` title="${escapeHtml(items.map(item => item.holiday_name).join(", "))}"` : "";
        cells.push(`
            <button type="button" class="holiday-day ${items.length ? "holiday-active" : ""} ${iso === todayIso ? "today" : ""}" data-holiday-date="${iso}"${holidayTitle}>
                <div class="holiday-day-number">${day}</div>
                <div class="holiday-badges">
                    ${items.length ? '<span class="holiday-badge">&bull;</span>' : ''}
                </div>
            </button>
        `);
    }
    holidayMonthLabel.textContent = holidayMonthCursor.toLocaleDateString("es-CL", {
        month: "long",
        year: "numeric"
    });
    holidayCalendar.innerHTML = [
        ...weekdayLabels.map(label => `<div class="holiday-weekday">${label}</div>`),
        ...cells
    ].join("");
}

async function loadHolidayCalendar() {
    const year = holidayMonthCursor.getFullYear();
    const month = holidayMonthCursor.getMonth() + 1;
    holidayEntries = await apiRequest(`/holidays?year=${year}&month=${month}`);
    renderHolidayCalendar();
}

async function refreshDisplayedSettlementsForHolidayChange() {
    if (currentContext && liquidationCycle.value && liquidationEmployee.value) {
        await loadSettlement();
        return;
    }
    if (currentView === "search" && selectedSearchCycleIds.length && selectedSearchEmployeeIds.length) {
        await loadSearchSettlement();
    }
}

async function loadDashboard() {
    if (!hasPermission("payroll.import")) {
        drImportBtn.classList.add("hidden");
        servicesImportBtn.classList.add("hidden");
    }
    const imports = await apiRequest("/imports");
    importsTableBody.innerHTML = imports.map(item => `
        <tr>
            <td>${new Date(item.imported_at).toLocaleDateString("es-CL")}</td>
            <td>${escapeHtml(item.file_name)}</td>
            <td><span class="tag ${item.source_type === "DR" ? "green-tag" : "blue-tag"}">${item.source_type}</span></td>
            <td>${item.rows_imported}</td>
            <td>${escapeHtml(item.imported_by)}</td>
        </tr>
    `).join("");
    await loadHolidayCalendar();
}

async function loadCycleDropdowns() {
    cyclesCache = await apiRequest("/cycles");
    const options = cyclesCache.map(cycle =>
        `<option value="${cycle.id}">${escapeHtml(cycle.cycle_name)}</option>`
    ).join("");
    liquidationCycle.innerHTML = options;
    ratesCycle.innerHTML = options;
    rateModalCycle.innerHTML = options;
    selectedSearchCycleIds = selectedSearchCycleIds.filter(cycleId =>
        cyclesCache.some(cycle => Number(cycle.id) === Number(cycleId))
    );
    if (!selectedSearchCycleIds.length && cyclesCache.length) {
        selectedSearchCycleIds = [Number(cyclesCache[0].id)];
    }
    renderSearchCycleChecklist();
    settlementCycleName.textContent = cyclesCache[0]?.cycle_name || "";
    await loadSearchEmployees();
    updateSearchActionState();
    if (currentView === "rates") {
        await loadRates();
    }
    if (currentContext) await loadSettlementEmployees();
}

async function runImport(sourceType, fileInput, button, confirmed = false) {
    const file = fileInput.files[0];
    if (!file) {
        alert("Seleccione un archivo Excel.");
        return;
    }
    const body = new FormData();
    body.append("confirm_reimport", String(confirmed));
    body.append("file", file);
    button.disabled = true;
    try {
        const importedFileName = file.name;
        showStatusModal({
            title: sourceType === "DR" ? "Importando D&R" : "Importando Servicios",
            message: `Procesando ${importedFileName}. Esto puede tardar unos segundos...`,
            loading: true,
            closable: false
        });
        const result = await apiRequest(`/imports/${sourceType}`, { method: "POST", body });
        showStatusModal({
            title: "Importacion completada",
            message: `${result.records_inserted} registros insertados${result.workers_created ? `, ${result.workers_created} trabajador(es) creados` : ""}.`,
            loading: false,
            closable: true
        });
        fileInput.value = "";
        if (sourceType === "DR") {
            updateImportSelection(
                drImportFile,
                drImportBtn,
                drImportSelected,
                "Importar D&R",
                drImportCard,
                true,
                importedFileName
            );
        } else {
            updateImportSelection(
                servicesImportFile,
                servicesImportBtn,
                servicesImportSelected,
                "Importar Servicios",
                servicesImportCard,
                true,
                importedFileName
            );
        }
        await loadDashboard();
        await loadCycleDropdowns();
    } catch (error) {
        const detail = error.detail;
        if (detail?.requires_confirmation && !confirmed) {
            hideStatusModal();
            const accepted = confirm(
                `${detail.message}\nPosibles reimportaciones: ${detail.possible_reimports}\nDesea continuar?`
            );
            if (accepted) await runImport(sourceType, fileInput, button, true);
        } else {
            showStatusModal({
                title: "Importacion con error",
                message: typeof detail === "string" ? detail : error.message,
                loading: false,
                closable: true
            });
        }
    } finally {
        button.disabled = false;
    }
}

function applyPermissions(user) {
    currentUser = user;
    document.querySelector(".profile-text strong").textContent = user.full_name;
    document.querySelector(".profile-text span").textContent = user.role;
    usersNav.classList.toggle("hidden", !hasPermission("users.manage"));
    if (newWorkerBtn) {
        newWorkerBtn.classList.toggle("hidden", user.role !== "ADMIN");
    }
    if (holidayNewBtn) {
        holidayNewBtn.classList.toggle("hidden", user.role !== "ADMIN");
    }
    searchEditBtn?.classList.add("hidden");
    searchAdjustmentsBtn?.classList.add("hidden");
}

function openSession(user) {
    applyPermissions(user);
    loginScreen.classList.add("hidden");
    appShell.classList.remove("hidden");
}

function closeSession() {
    localStorage.removeItem("payroll_access_token");
    currentUser = null;
    appShell.classList.add("hidden");
    loginScreen.classList.remove("hidden");
    loginPassword.value = "";
}

function initializeRememberedLogin() {
    const rememberedUsername = localStorage.getItem(rememberedUsernameKey);
    if (rememberedUsername) {
        loginUsername.value = rememberedUsername;
        if (loginRemember) {
            loginRemember.checked = true;
        }
    }
}

async function loadUsers() {
    if (!hasPermission("users.manage")) return;
    const users = await apiRequest("/users");
    usersTableBody.innerHTML = users.map(user => `
        <tr>
            <td>${escapeHtml(user.username)}</td>
            <td>${escapeHtml(user.full_name)}</td>
            <td><span class="tag ${user.role === "ADMIN" ? "green-tag" : "blue-tag"}">${user.role}</span></td>
            <td>${user.active ? "Activo" : "Inactivo"}</td>
            <td></td>
        </tr>
    `).join("");
}

function resetWorkerForm() {
    editingWorkerId = null;
    workerName.value = "";
    workerContract.value = "";
    workerRut.value = "";
    workerEmail.value = "";
    workerCargo.value = "";
    workerName.disabled = false;
    workerModal.classList.add("hidden");
}

function openWorkerModal({ name = "", contractType = "", rut = "", email = "", cargo = "", readOnlyName = false } = {}) {
    workerName.value = name;
    workerContract.value = contractType || "";
    workerRut.value = rut || "";
    workerEmail.value = email || "";
    workerCargo.value = cargo || "";
    workerName.disabled = readOnlyName;
    workerModal.classList.remove("hidden");
}

function selectedSearchEmployeeName() {
    return selectedEmployeeNames()[0] || "";
}

function resetAdjustmentForm() {
    selectedAdjustmentId = null;
    adjustmentType.value = "BONUS";
    adjustmentUnits.value = "";
    adjustmentAmount.value = "";
    adjustmentObservations.value = "";
    adjustmentSaveBtn.textContent = "Crear ajuste";
    adjustmentDeleteBtn.classList.add("hidden");
}

function fillAdjustmentForm(adjustment) {
    selectedAdjustmentId = adjustment.id;
    adjustmentType.value = adjustment.adjustment_type;
    adjustmentUnits.value = adjustment.units === null ? "" : Math.round(Number(adjustment.units));
    adjustmentAmount.value = adjustment.amount === null ? "" : Math.round(Number(adjustment.amount));
    adjustmentObservations.value = adjustment.observations ?? "";
    adjustmentSaveBtn.textContent = "Editar ajuste";
    adjustmentDeleteBtn.classList.toggle("hidden", !adjustment.active);
}

function renderAdjustmentsTable() {
    adjustmentsTableBody.innerHTML = manualAdjustments.length
        ? manualAdjustments.map(item => `
            <tr>
                <td>${escapeHtml(adjustmentTypeLabel(item.adjustment_type))}</td>
                <td>${item.units === null ? "" : unitValue(item.units)}</td>
                <td>${money(item.amount)}</td>
                <td>${item.active ? "Activo" : "Eliminado"}</td>
                <td>
                    <div class="actions left">
                        ${currentUser?.role === "ADMIN"
                            ? `<button class="btn secondary small-btn adjustment-edit-btn" data-adjustment-id="${item.id}" ${item.active ? "" : "disabled"}>Editar</button>`
                            : ""}
                    </div>
                </td>
            </tr>
        `).join("")
        : '<tr><td colspan="5">No hay ajustes registrados.</td></tr>';
}

async function loadManualAdjustments() {
    if (!isSingleSearchSelection()) {
        manualAdjustments = [];
        renderAdjustmentsTable();
        return;
    }
    manualAdjustments = await apiRequest(
        `/manual-adjustments?cycle_id=${selectedSearchCycleIds[0]}&employee_id=${selectedSearchEmployeeIds[0]}`
    );
    renderAdjustmentsTable();
}

function openAdjustmentsModal() {
    adjustmentWorker.value = selectedSearchEmployeeName();
    adjustmentCycle.value = cycleNameById(selectedSearchCycleIds[0]);
    resetAdjustmentForm();
    adjustmentsModal.classList.remove("hidden");
    loadManualAdjustments().catch(error => alert(error.message));
}

function closeAdjustmentsModal() {
    adjustmentsModal.classList.add("hidden");
    resetAdjustmentForm();
    manualAdjustments = [];
    adjustmentsTableBody.innerHTML = "";
}

async function exportSearchSettlement(fileFormat) {
    if (displayedSearchSettlements.length > 1) {
        for (const item of displayedSearchSettlements) {
            const query = new URLSearchParams({
                cycle_id: item.cycleId,
                employee_id: item.employeeId,
                file_format: fileFormat
            });
            await downloadApiFile(`/exports/settlement?${query}`);
        }
        return;
    }
    if (!isSingleSearchSelection()) {
        alert("Seleccione al menos una planilla para exportar.");
        return;
    }
    const query = new URLSearchParams({
        cycle_id: selectedSearchCycleIds[0],
        employee_id: selectedSearchEmployeeIds[0],
        file_format: fileFormat
    });
    await downloadApiFile(`/exports/settlement?${query}`);
}

async function focusSearchSettlement(cycleId, employeeId) {
    selectedSearchCycleIds = [Number(cycleId)];
    selectedSearchEmployeeIds = [Number(employeeId)];
    renderSearchCycleChecklist();
    await loadSearchEmployees();
    updateSearchActionState();
    await loadSearchSettlement();
}

async function exportContextSettlement(fileFormat) {
    if (!currentContext || !liquidationCycle.value || !liquidationEmployee.value) {
        alert("Seleccione ciclo y trabajador.");
        return;
    }
    if (liquidationEmployee.value === "__ALL__") {
        alert("Para exportar Excel seleccione un trabajador especifico o use Exportar PDF para la vista completa.");
        return;
    }
    const query = new URLSearchParams({
        cycle_id: liquidationCycle.value,
        employee_id: liquidationEmployee.value,
        cost_center: currentContext.costCenter,
        role_type: currentContext.roleType,
        file_format: fileFormat
    });
    await downloadApiFile(`/exports/settlement?${query}`);
}

async function loadWorkers() {
    const workers = await apiRequest("/workers");
    workersTableBody.innerHTML = workers.map(worker => `
        <tr>
            <td>${escapeHtml(worker.employee_name)}</td>
            <td>${escapeHtml(worker.cargo || "")}</td>
            <td>${escapeHtml(worker.rut || "")}</td>
            <td>${escapeHtml(worker.email || "")}</td>
            <td>${editingWorkerId === worker.id
                ? `<div class="actions left">
                        <button class="btn secondary small-btn choose-worker-contract-btn" data-worker-id="${worker.id}" data-contract-type="NEW">Nuevo</button>
                        <button class="btn secondary small-btn choose-worker-contract-btn" data-worker-id="${worker.id}" data-contract-type="OLD">Antiguo</button>
                        <button class="btn secondary small-btn cancel-worker-inline-btn" data-worker-id="${worker.id}">Cancelar</button>
                   </div>`
                : escapeHtml(contractLabel(worker.contract_type))}</td>
            <td>${currentUser?.role === "ADMIN"
                ? editingWorkerId === worker.id
                    ? '<span class="rate-readonly">Seleccione contrato</span>'
                    : `<div class="actions left">
                            <button class="btn secondary small-btn edit-worker-btn"
                                data-worker-id="${worker.id}"
                                data-worker-name="${escapeHtml(worker.employee_name)}"
                                data-contract-type="${worker.contract_type || ""}"
                                data-worker-rut="${escapeHtml(worker.rut || "")}"
                                data-worker-email="${escapeHtml(worker.email || "")}"
                                data-worker-cargo="${escapeHtml(worker.cargo || "")}">
                                Editar
                            </button>
                            <button class="btn danger small-btn delete-worker-btn"
                                data-worker-id="${worker.id}"
                                data-worker-name="${escapeHtml(worker.employee_name)}">
                                Eliminar
                            </button>
                        </div>`
                : '<span class="rate-readonly">Solo lectura</span>'}</td>
        </tr>
    `).join("");
}

async function refreshAfterWorkerContractChange() {
    await loadWorkers();
    await loadSearchEmployees();
    if (currentContext) {
        await loadSettlementEmployees();
    }
    if (currentView === "search" && isSingleSearchSelection()) {
        await loadSearchSettlement();
    }
}

async function loadSearchEmployees() {
    if (!selectedSearchCycleIds.length) {
        selectedSearchEmployeeIds = [];
        renderSearchEmployeeChecklist([]);
        updateSearchActionState();
        if (currentView === "search") {
            setActiveSheet({
                mode: "search",
                container: spreadsheetSearch,
                employeeNameEl: searchSettlementEmployeeName,
                cycleNameEl: searchSettlementCycleName,
                context: null
            });
            clearSettlement();
        }
        return;
    }

    const employeesByName = new Map();
    for (const cycleId of selectedSearchCycleIds) {
        const query = new URLSearchParams({
            cycle_from_id: cycleId,
            cycle_to_id: cycleId
        });
        const employees = await apiRequest(`/search/employees?${query}`);
        for (const employee of employees) {
            if (!employeesByName.has(employee.employee_name)) {
                employeesByName.set(employee.employee_name, employee);
            }
        }
    }
    const employees = [...employeesByName.values()].sort((a, b) =>
        a.employee_name.localeCompare(b.employee_name, "es")
    );
    selectedSearchEmployeeIds = selectedSearchEmployeeIds.filter(employeeId =>
        employees.some(employee => Number(employee.id) === Number(employeeId))
    );
    renderSearchEmployeeChecklist(employees);
    updateSearchActionState();
    if (currentView === "search") {
        clearSettlement();
    }
}

const contexts = {
    "dr-drivers": {title:"Liquidaciones D&R Choferes", centerLabel:"D&R", costCenter:"DR", roleLabel:"Chofer", roleType:"DRIVER"},
    "dr-assistants": {title:"Liquidaciones D&R Auxiliares", centerLabel:"D&R", costCenter:"DR", roleLabel:"Auxiliar", roleType:"ASSISTANT"},
    "services-drivers": {title:"Liquidaciones Servicios Choferes", centerLabel:"SERVICES", costCenter:"SERVICES", roleLabel:"Chofer", roleType:"DRIVER"},
    "services-assistants": {title:"Liquidaciones Servicios Auxiliares", centerLabel:"SERVICES", costCenter:"SERVICES", roleLabel:"Auxiliar", roleType:"ASSISTANT"}
};

const rateContexts = {
    "dr-driver-old": {costCenter:"DR", roleType:"DRIVER", contractType:"OLD"},
    "dr-driver-new": {costCenter:"DR", roleType:"DRIVER", contractType:"NEW"},
    "dr-assistant-old": {costCenter:"DR", roleType:"ASSISTANT", contractType:"OLD"},
    "dr-assistant-new": {costCenter:"DR", roleType:"ASSISTANT", contractType:"NEW"},
    "services-driver-old": {costCenter:"SERVICES", roleType:"DRIVER", contractType:"OLD"},
    "services-driver-new": {costCenter:"SERVICES", roleType:"DRIVER", contractType:"NEW"},
    "services-assistant-old": {costCenter:"SERVICES", roleType:"ASSISTANT", contractType:"OLD"},
    "services-assistant-new": {costCenter:"SERVICES", roleType:"ASSISTANT", contractType:"NEW"}
};

function cycleNameById(cycleId) {
    return cyclesCache.find(cycle => Number(cycle.id) === Number(cycleId))?.cycle_name || "";
}

function contractLabel(contractType) {
    if (contractType === "OLD") return "Antiguo";
    if (contractType === "NEW") return "Nuevo";
    return "Sin definir";
}

function selectedRateApplyMode() {
    return document.querySelector('input[name="rate-apply-mode"]:checked')?.value || "SINGLE_CYCLE";
}

function updateContextActionState() {
    const hasSelection = Boolean(currentContext && liquidationCycle.value && liquidationEmployee.value);
    liquidationExportExcelBtn.disabled = !hasSelection;
    liquidationExportPdfBtn.disabled = !hasSelection;
    liquidationEmailBtn.disabled = !hasSelection;
    liquidationSoftlandBtn.disabled = !hasSelection;
}

function settlementCycleDate(columnIndex) {
    return dates[columnIndex]?.[3] || null;
}

let dates = [];
let rows = [];
let selectedSearchCycleIds = [];
let selectedSearchEmployeeIds = [];
let displayedSearchSettlements = [];
let editModalCycleId = null;
let editModalEmployeeId = null;
let editModalDates = [];
let editModalRows = [];

function checkedValues(container, key) {
    const attr = key.replace(/[A-Z]/g, char => `-${char.toLowerCase()}`);
    return [...container.querySelectorAll(`input[data-${attr}]:checked`)].map(input => Number(input.dataset[key]));
}

function selectedCycleObjects() {
    return cyclesCache.filter(cycle => selectedSearchCycleIds.includes(Number(cycle.id)));
}

function selectedEmployeeNames() {
    return [...searchEmployee.querySelectorAll("input[data-employee-id]:checked")]
        .map(input => input.dataset.employeeName)
        .filter(Boolean);
}

function isSingleSearchSelection() {
    return selectedSearchCycleIds.length === 1 && selectedSearchEmployeeIds.length === 1;
}

function updateSearchActionState() {
    const single = isSingleSearchSelection();
    searchEditBtn?.classList.add("hidden");
    searchAdjustmentsBtn?.classList.add("hidden");
    searchSingleActions?.classList.toggle("hidden", !(single && currentUser?.role === "ADMIN"));
    searchExportExcelBtn.disabled = !displayedSearchSettlements.length && !single;
    searchExportPdfBtn.disabled = !displayedSearchSettlements.length && !single;
    searchEmailBtn.disabled = !displayedSearchSettlements.length && !single;
    searchSoftlandBtn.disabled = !displayedSearchSettlements.length && !single;
}

function closeSearchDropdowns() {
    searchCycle.classList.add("hidden");
    searchEmployee.classList.add("hidden");
}

function positionSearchDropdown(panel, anchor) {
    const rect = anchor.getBoundingClientRect();
    panel.style.top = `${rect.bottom + 6}px`;
    panel.style.left = `${rect.left}px`;
    panel.style.width = `${rect.width}px`;
}

function toggleSearchDropdown(panel, anchor) {
    const shouldOpen = panel.classList.contains("hidden");
    closeSearchDropdowns();
    if (shouldOpen) {
        positionSearchDropdown(panel, anchor);
        panel.classList.remove("hidden");
    }
}

function renderSearchCycleChecklist() {
    searchCycle.innerHTML = cyclesCache.length
        ? cyclesCache.map(cycle => `
            <label class="checklist-item">
                <input type="checkbox" data-cycle-id="${cycle.id}" ${selectedSearchCycleIds.includes(Number(cycle.id)) ? "checked" : ""} />
                <span>${escapeHtml(cycle.cycle_name)}</span>
            </label>
        `).join("")
        : '<div class="checklist-empty">No hay ciclos disponibles.</div>';
    searchCycleSummary.textContent = selectedSearchCycleIds.length
        ? `${selectedSearchCycleIds.length} ciclo(s) seleccionado(s)`
        : "Seleccione uno o más ciclos";
}

function renderSearchEmployeeChecklist(employees) {
    searchEmployee.innerHTML = employees.length
        ? [
            `<label class="checklist-item checklist-item-all">
                <input
                    type="checkbox"
                    data-select-all-employees="true"
                    ${employees.length && selectedSearchEmployeeIds.length === employees.length ? "checked" : ""} />
                <span>Todos</span>
            </label>`,
            ...employees.map(employee => `
                <label class="checklist-item">
                    <input
                        type="checkbox"
                        data-employee-id="${employee.id}"
                        data-employee-name="${escapeHtml(employee.employee_name)}"
                        ${selectedSearchEmployeeIds.includes(Number(employee.id)) ? "checked" : ""} />
                    <span>${escapeHtml(employee.employee_name)}</span>
                </label>
            `)
        ].join("")
        : '<div class="checklist-empty">Seleccione primero uno o más ciclos.</div>';
    searchEmployeeSummary.textContent = selectedSearchEmployeeIds.length
        ? selectedSearchEmployeeIds.length === employees.length
            ? "Todos los trabajadores"
            : `${selectedSearchEmployeeIds.length} trabajador(es) seleccionado(s)`
        : "Seleccione uno o más trabajadores";
}

function setActiveSheet({ mode, container, employeeNameEl, cycleNameEl, context }) {
    activeSheetMode = mode;
    activeSheetContainer = container;
    activeSheetEmployeeName = employeeNameEl;
    activeSheetCycleName = cycleNameEl;
    activeSheetContext = context;
}

function clearSettlement() {
    dates = [];
    rows = [];
    activeSheetEmployeeName.textContent = "";
    activeSheetCycleName.textContent = "";
    renderSpreadsheet(activeSheetContainer);
}

function settlementToSheetData(settlement, contextOverride = null) {
    const statuses = new Map(settlement.statuses.map(item => [item.date, formatStatusLabel(item.status)]));
    const sheetDates = settlement.dates.map(item => [
        item.label,
        item.weekday,
        statuses.get(item.date) || "",
        item.date,
        Boolean(item.is_holiday),
        item.holiday_names || []
    ]);
    const sheetRows = [
        {label:"Estado", units:"", rate:"", total:"", values:sheetDates.map(item => item[2]), status:true},
        ...settlement.rows.map(row => ({
            rowType: row.row_type,
            conceptId: row.concept_id,
            label: row.concept_name,
            units: row.units,
            rate: row.rate,
            totalOverride: row.total,
            values: row.daily_values.map(item => item.value),
            originalValues: row.daily_values.map(item => item.value),
            totalRow: row.row_type === "total_to_pay" || row.row_type === "production_total",
            summary: row.row_type !== "concept" && row.row_type !== "total_to_pay" && row.row_type !== "production_total"
        }))
    ];
    return {
        employeeName: settlement.employee.employee_name,
        cycleName: settlement.cycle.cycle_name,
        roleLabel: contextOverride?.roleLabel || activeSheetContext?.roleLabel || "",
        centerLabel: contextOverride?.centerLabel || activeSheetContext?.centerLabel || "",
        dates: sheetDates,
        rows: sheetRows
    };
}

function closeSearchEditModal() {
    searchEditModal.classList.add("hidden");
    editModalCycleId = null;
    editModalEmployeeId = null;
    editModalDates = [];
    editModalRows = [];
    searchEditSpreadsheet.innerHTML = "";
}

function renderSearchEditModalSpreadsheet() {
    searchEditSpreadsheet.innerHTML = renderSpreadsheetMarkup(
        {
            employeeName: searchEditEmployeeName.textContent || "",
            roleLabel: "Consolidado",
            dates: editModalDates,
            rows: editModalRows
        },
        true
    );
}

function editModalCycleDate(columnIndex) {
    return editModalDates[columnIndex]?.[3] || null;
}

async function openSearchEditModal(cycleId, employeeId) {
    const query = new URLSearchParams({
        cycle_id: Number(cycleId),
        employee_id: Number(employeeId)
    });
    const settlement = await apiRequest(`/liquidations?${query}`);
    const sheetData = settlementToSheetData(settlement, {
        centerLabel: "D&R + Servicios",
        roleLabel: "Consolidado"
    });
    editModalCycleId = Number(cycleId);
    editModalEmployeeId = Number(employeeId);
    editModalDates = sheetData.dates;
    editModalRows = sheetData.rows;
    searchEditEmployeeName.textContent = settlement.employee.employee_name;
    searchEditCycleName.textContent = settlement.cycle.cycle_name;
    renderSearchEditModalSpreadsheet();
    searchEditModal.classList.remove("hidden");
}

function renderSpreadsheetMarkup(sheetData, allowEdit = false) {
    const employeeName = sheetData.employeeName || "";
    const roleLabel = sheetData.roleLabel || "";
    let html = `<table class="sheet-table"><thead>
        <tr>
            <th class="fixed">${escapeHtml(employeeName)}</th>
            <th class="units">${escapeHtml(employeeName)}<br>Unidades</th>
            <th class="rate">Tarifa</th>
            <th class="total">${escapeHtml(roleLabel)}<br>Total $</th>
            ${sheetData.dates.map(d => `<th class="date-head ${d[4] ? "holiday-head" : ""}"${d[4] && d[5]?.length ? ` title="${escapeHtml(d[5].join(", "))}"` : ""}>${d[0]}</th>`).join("")}
        </tr>
        <tr>
            <th class="fixed">Actividad</th>
            <th class="units"></th>
            <th class="rate"></th>
            <th class="total"></th>
            ${sheetData.dates.map(d => `<th class="date-head ${d[4] ? "holiday-head" : ""}"${d[4] && d[5]?.length ? ` title="${escapeHtml(d[5].join(", "))}"` : ""}>${d[1]}</th>`).join("")}
        </tr>
    </thead><tbody>`;

    sheetData.rows.forEach((row, rIndex) => {
        if (row.empty) {
            html += `<tr><td class="fixed"></td><td class="units"></td><td class="rate"></td><td class="total"></td>${sheetData.dates.map(()=>"<td></td>").join("")}</tr>`;
            return;
        }
        const cls = row.section ? "section" : row.totalRow ? "total-row" : row.summary ? "summary-row" : "";
        html += `<tr class="${cls}">
            <td class="fixed ${row.section ? "section" : row.totalRow ? "summary-label" : ""}">${row.label}</td>
            <td class="units">${unitValue(row.units)}</td>
            <td class="rate">${money(row.rate)}</td>
            <td class="total" ${row.totalRow ? "data-total-to-pay" : `data-total-row="${rIndex}"`}>${money(rowTotal(row))}</td>`;

        sheetData.dates.forEach((d, cIndex) => {
            const val = row.values ? row.values[cIndex] ?? "" : "";
            const holidayClass = d[4] ? "holiday-cell" : "";
            const holidayTitle = d[4] && d[5]?.length ? ` title="${escapeHtml(d[5].join(", "))}"` : "";
            const blue = row.status || row.totalRow || row.summary ? "blue" : "";
            if (row.status) {
                html += `<td class="status-head ${holidayClass}"${holidayTitle}>${val}</td>`;
            } else if (allowEdit && row.conceptId) {
                html += `<td class="${`${blue} ${holidayClass}`.trim()}"${holidayTitle}>
                    <input
                        class="cell-input"
                        type="number"
                        min="0"
                        step="1"
                        value="${val === "" || val === null || val === undefined ? "" : Math.round(Number(val))}"
                        data-row="${rIndex}"
                        data-col="${cIndex}">
                </td>`;
            } else {
                html += `<td class="${`${blue} ${holidayClass}`.trim()}"${holidayTitle}>${unitValue(val)}</td>`;
            }
        });
        html += `</tr>`;
    });

    html += `</tbody></table>`;
    return html;
}

function applySettlement(settlement) {
    const sheetData = settlementToSheetData(settlement);
    dates = sheetData.dates;
    rows = sheetData.rows;
    activeSheetEmployeeName.textContent = settlement.employee.employee_name;
    activeSheetCycleName.textContent = settlement.cycle.cycle_name;
    renderSpreadsheet(activeSheetContainer);
}

function openRateModal(row) {
    currentRateRow = row;
    rateModalConcept.value = row.concept_name;
    rateModalCurrent.value = row.amount === null ? "Sin tarifa" : money(row.amount);
    rateModalAmount.value = row.amount ?? "";
    rateModalCycle.value = ratesCycle.value || cyclesCache[0]?.id || "";
    document.querySelector('input[name="rate-apply-mode"][value="SINGLE_CYCLE"]').checked = true;
    rateModal.classList.remove("hidden");
}

function closeRateModal() {
    currentRateRow = null;
    rateModal.classList.add("hidden");
}

async function loadRates() {
    const ctx = rateContexts[currentRatesContext];
    if (!ctx || !ratesCycle.value) {
        ratesTableBody.innerHTML = "";
        return;
    }
    const query = new URLSearchParams({
        cost_center: ctx.costCenter,
        role_type: ctx.roleType,
        cycle_id: ratesCycle.value,
        contract_type: ctx.contractType
    });
    const rows = await apiRequest(`/rates?${query}`);
    ratesTableBody.innerHTML = rows.map(row => `
        <tr>
            <td>${escapeHtml(row.concept_name)}</td>
            <td>${row.amount === null ? '<span class="rate-readonly">Sin tarifa</span>' : money(row.amount)}</td>
            <td>${escapeHtml(row.effective_from_cycle_name || "Sin vigencia")}</td>
            <td>${escapeHtml(row.effective_to_cycle_name || "En adelante")}</td>
            <td>${currentUser?.role === "ADMIN"
                ? `<button class="btn secondary small-btn edit-rate-btn"
                        data-rate-id="${row.rate_id ?? ""}"
                        data-concept-id="${row.concept_id}"
                        data-concept-name="${escapeHtml(row.concept_name)}"
                        data-amount="${row.amount ?? ""}"
                        data-contract-type="${row.contract_type || ""}">
                        Editar
                   </button>`
                : '<span class="rate-readonly">Solo lectura</span>'}</td>
        </tr>
    `).join("");
}

async function refreshSettlementIfNeeded(costCenter, roleType, cycleId) {
    if (!currentContext) return;
    if (currentContext.costCenter !== costCenter || currentContext.roleType !== roleType) return;
    if (Number(liquidationCycle.value) !== Number(cycleId) || !liquidationEmployee.value) return;
    await loadSettlement();
}

async function loadSettlement() {
    if (!currentContext || !liquidationCycle.value || !liquidationEmployee.value) {
        setActiveSheet({
            mode: "context",
            container: spreadsheet,
            employeeNameEl: settlementEmployeeName,
            cycleNameEl: settlementCycleName,
            context: currentContext
        });
        clearSettlement();
        updateContextActionState();
        return;
    }
    setActiveSheet({
        mode: "context",
        container: spreadsheet,
        employeeNameEl: settlementEmployeeName,
        cycleNameEl: settlementCycleName,
        context: currentContext
    });
    updateContextActionState();
    if (liquidationEmployee.value === "__ALL__") {
        const settlements = [];
        for (const employee of contextEmployeesCache) {
            const query = new URLSearchParams({
                cycle_id: liquidationCycle.value,
                employee_id: employee.id,
                cost_center: currentContext.costCenter,
                role_type: currentContext.roleType
            });
            try {
                settlements.push(await apiRequest(`/settlements?${query}`));
            } catch (error) {
                if (!String(error.message || "").includes("No existen registros")) {
                    throw error;
                }
            }
        }
        if (!settlements.length) {
            clearSettlement();
            return;
        }
        renderContextSettlementStack(settlements);
        return;
    }
    const query = new URLSearchParams({
        cycle_id: liquidationCycle.value,
        employee_id: liquidationEmployee.value,
        cost_center: currentContext.costCenter,
        role_type: currentContext.roleType
    });
    applySettlement(await apiRequest(`/settlements?${query}`));
}

async function loadSearchSettlement() {
    const context = {
        centerLabel: "D&R + Servicios",
        costCenter: null,
        roleLabel: "Consolidado",
        roleType: null
    };
    setActiveSheet({
        mode: "search",
        container: spreadsheetSearch,
        employeeNameEl: searchSettlementEmployeeName,
        cycleNameEl: searchSettlementCycleName,
        context
    });
    searchSettlementCenter.textContent = context.centerLabel;
    searchSettlementRole.textContent = context.roleLabel;
    if (!selectedSearchCycleIds.length || !selectedSearchEmployeeIds.length) {
        displayedSearchSettlements = [];
        clearSettlement();
        searchResultTitle.textContent = "Liquidacion";
        return;
    }
    if (isSingleSearchSelection()) {
        const query = new URLSearchParams({
            cycle_id: selectedSearchCycleIds[0],
            employee_id: selectedSearchEmployeeIds[0]
        });
        const settlement = await apiRequest(`/liquidations?${query}`);
        displayedSearchSettlements = [{
            cycleId: Number(selectedSearchCycleIds[0]),
            employeeId: Number(selectedSearchEmployeeIds[0])
        }];
        searchResultTitle.textContent = `Liquidacion ${settlement.employee.employee_name}`;
        applySettlement(settlement);
        updateSearchActionState();
        return;
    }

    const cycleGroups = [];
    for (const cycle of selectedCycleObjects()) {
        const settlements = [];
        for (const employeeId of selectedSearchEmployeeIds) {
            const query = new URLSearchParams({
                cycle_id: cycle.id,
                employee_id: employeeId
            });
            try {
                const settlement = await apiRequest(`/liquidations?${query}`);
                settlements.push(settlement);
            } catch (error) {
                if (!String(error.message || "").includes("No existen registros")) {
                    throw error;
                }
            }
        }
        if (settlements.length) {
            cycleGroups.push({ cycle, settlements });
        }
    }

    editMode = false;
    searchSaveBtn.classList.add("hidden");
    searchCancelEditBtn.classList.add("hidden");
    searchEditBtn?.classList.add("hidden");
    searchResultTitle.textContent = "Liquidaciones seleccionadas";
    searchSettlementEmployeeName.textContent = "";
    searchSettlementCycleName.textContent = "";
    searchSettlementCenter.textContent = "D&R + Servicios";
    searchSettlementRole.textContent = "Consolidado";
    if (!cycleGroups.length) {
        spreadsheetSearch.innerHTML = '<div class="checklist-empty">No se encontraron liquidaciones para la seleccion actual.</div>';
        updateSearchActionState();
        return;
    }
    displayedSearchSettlements = cycleGroups.flatMap(group =>
        group.settlements.map(settlement => ({
            cycleId: Number(group.cycle.id),
            employeeId: Number(settlement.employee.id)
        }))
    );
    spreadsheetSearch.innerHTML = cycleGroups.map(group => `
        <section class="stack-cycle-group">
            <h3 class="stack-cycle-title">${escapeHtml(group.cycle.cycle_name)}</h3>
            ${group.settlements.map(settlement => {
                const sheetData = settlementToSheetData(settlement, {
                    centerLabel: "D&R + Servicios",
                    roleLabel: "Consolidado"
                });
                return `
                    <article class="stack-settlement-card">
                        <div class="settlement-meta">
                            <strong>${escapeHtml(settlement.employee.employee_name)}</strong>
                            <span>Vista: <b>Consolidado</b></span>
                            <span>Centro: <b>D&R + Servicios</b></span>
                            <span>Ciclo: <b>${escapeHtml(settlement.cycle.cycle_name)}</b></span>
                            ${currentUser?.role === "ADMIN" ? `
                                <div class="stack-settlement-actions">
                                    <button class="btn secondary small-btn stack-edit-btn" data-cycle-id="${group.cycle.id}" data-employee-id="${settlement.employee.id}">Editar</button>
                                    <button class="btn secondary small-btn stack-adjustments-btn" data-cycle-id="${group.cycle.id}" data-employee-id="${settlement.employee.id}">Ajustes</button>
                                </div>
                            ` : ""}
                        </div>
                        <div class="spreadsheet">
                            ${renderSpreadsheetMarkup(sheetData, false)}
                        </div>
                    </article>
                `;
            }).join("")}
        </section>
    `).join("");
    updateSearchActionState();
}

function renderContextSettlementStack(settlements) {
    settlementEmployeeName.textContent = settlements.length === 1 ? settlements[0].employee.employee_name : "Todos";
    spreadsheet.innerHTML = `
        <section class="stack-cycle-group">
            ${settlements.map(settlement => {
                const sheetData = settlementToSheetData(settlement, currentContext);
                return `
                    <article class="stack-settlement-card">
                        <div class="settlement-meta">
                            <strong>${escapeHtml(settlement.employee.employee_name)}</strong>
                            <span>Tarifa: <b>${escapeHtml(currentContext?.roleLabel || "")}</b></span>
                            <span>Centro: <b>${escapeHtml(currentContext?.centerLabel || "")}</b></span>
                            <span>Ciclo: <b>${escapeHtml(settlement.cycle.cycle_name)}</b></span>
                        </div>
                        <div class="spreadsheet">
                            ${renderSpreadsheetMarkup(sheetData, false)}
                        </div>
                    </article>
                `;
            }).join("")}
        </section>
    `;
}

async function loadSettlementEmployees() {
    if (!currentContext || !liquidationCycle.value) {
        contextEmployeesCache = [];
        liquidationEmployee.innerHTML = "";
        clearSettlement();
        updateContextActionState();
        return;
    }
    const query = new URLSearchParams({
        cycle_id: liquidationCycle.value,
        cost_center: currentContext.costCenter,
        role_type: currentContext.roleType
    });
    const employees = await apiRequest(`/settlements/employees?${query}`);
    contextEmployeesCache = employees;
    liquidationEmployee.innerHTML = [
        '<option value="__ALL__">Todos</option>',
        ...employees.map(employee =>
        `<option value="${employee.id}">${escapeHtml(employee.employee_name)}</option>`
        )
    ].join("");
    if (employees.length) {
        liquidationEmployee.value = "__ALL__";
        await loadSettlement();
    } else {
        clearSettlement();
    }
    updateContextActionState();
}

function formatNumber(value, maximumFractionDigits = 0) {
    if (value === "" || value === undefined || value === null) return "";
    const number = Number(value);
    if (!Number.isFinite(number)) return "";
    return number.toLocaleString("es-CL", {
        minimumFractionDigits: 0,
        maximumFractionDigits
    });
}

function money(value) {
    return formatNumber(value, 0);
}

function unitValue(value) {
    return formatNumber(value, 0);
}

function rowTotal(row) {
    if (row.totalOverride !== undefined) return row.totalOverride;
    if (!row.rate || !row.units) return "";
    return row.units * row.rate;
}

function renderSpreadsheet(container) {
    container.innerHTML = renderSpreadsheetMarkup(
        {
            employeeName: activeSheetEmployeeName.textContent || "",
            roleLabel: activeSheetContext?.roleLabel || "",
            dates,
            rows
        },
        editMode
    );
}

function setView(viewId) {
    currentView = viewId;
    editMode = false;
    if (!adjustmentsModal.classList.contains("hidden")) {
        closeAdjustmentsModal();
    }
    views.forEach(v => v.classList.remove("active"));
    navItems.forEach(n => n.classList.remove("active"));
    const activeNav = document.querySelector(`[data-view="${viewId}"]`);
    if (activeNav) activeNav.classList.add("active");
    searchSaveBtn.classList.add("hidden");
    searchCancelEditBtn.classList.add("hidden");
    searchEditBtn?.classList.add("hidden");
    searchAdjustmentsBtn?.classList.add("hidden");

    if (viewId === "dashboard") {
        currentContext = null;
        document.getElementById("dashboard").classList.add("active");
        title.textContent = "Dashboard";
        breadcrumb.textContent = "Dashboard";
        loadDashboard().catch(error => alert(error.message));
        return;
    }

    if (viewId === "rates") {
        currentContext = null;
        document.getElementById("rates").classList.add("active");
        title.textContent = "Tarifas";
        breadcrumb.textContent = "Tarifas";
        loadRates().catch(error => alert(error.message));
        return;
    }

    if (viewId === "workers") {
        currentContext = null;
        document.getElementById("workers").classList.add("active");
        title.textContent = "Trabajadores";
        breadcrumb.textContent = "Trabajadores";
        resetWorkerForm();
        loadWorkers().catch(error => alert(error.message));
        return;
    }

    if (viewId === "search") {
        currentContext = null;
        document.getElementById("search").classList.add("active");
        title.textContent = "Liquidaciones";
        breadcrumb.textContent = "Liquidaciones";
        setActiveSheet({
            mode: "search",
            container: spreadsheetSearch,
            employeeNameEl: searchSettlementEmployeeName,
            cycleNameEl: searchSettlementCycleName,
            context: null
        });
        searchResultTitle.textContent = "Liquidacion";
        renderSpreadsheet(spreadsheetSearch);
        return;
    }

    if (viewId === "users") {
        if (!hasPermission("users.manage")) return;
        currentContext = null;
        document.getElementById("users").classList.add("active");
        title.textContent = "Usuarios";
        breadcrumb.textContent = "Usuarios";
        loadUsers().catch(error => alert(error.message));
        return;
    }

    const ctx = contexts[viewId];
    currentContext = ctx;
    liquidationView.classList.add("active");
    title.textContent = ctx.title;
    breadcrumb.textContent = ctx.title;
    liquidationPanelTitle.textContent = ctx.title;
    document.getElementById("settlement-center").textContent = ctx.centerLabel;
    document.getElementById("settlement-role").textContent = ctx.roleLabel;
    loadSettlementEmployees().catch(error => {
        clearSettlement();
        alert(error.message);
    });
}

loginBtn.addEventListener("click", async () => {
    loginBtn.disabled = true;
    try {
        const session = await apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify({
                username: loginUsername.value,
                password: loginPassword.value
            })
        });
        localStorage.setItem("payroll_access_token", session.access_token);
        if (loginRemember?.checked) {
            localStorage.setItem(rememberedUsernameKey, loginUsername.value.trim());
        } else {
            localStorage.removeItem(rememberedUsernameKey);
        }
        openSession(session.user);
        await Promise.all([loadDashboard(), loadCycleDropdowns()]);
        setView("dashboard");
    } catch (error) {
        alert(error.message);
    } finally {
        loginBtn.disabled = false;
    }
});

loginPassword.addEventListener("keydown", event => {
    if (event.key === "Enter") loginBtn.click();
});

loginShowPassword?.addEventListener("change", () => {
    loginPassword.type = loginShowPassword.checked ? "text" : "password";
});

logoutBtn.addEventListener("click", closeSession);

toggleSidebar.addEventListener("click", () => {
    appShell.classList.toggle("sidebar-collapsed");
});

navItems.forEach(item => {
    item.addEventListener("click", () => setView(item.dataset.view));
});

searchEditBtn?.addEventListener("click", () => {
    if (currentUser?.role !== "ADMIN" || activeSheetMode !== "search" || !isSingleSearchSelection()) return;
    editMode = true;
    searchEditBtn?.classList.add("hidden");
    searchSaveBtn.classList.remove("hidden");
    searchCancelEditBtn.classList.remove("hidden");
    renderSpreadsheet(activeSheetContainer);
});

searchAdjustmentsBtn?.addEventListener("click", () => {
    if (currentUser?.role !== "ADMIN") return;
    if (!isSingleSearchSelection()) {
        alert("Seleccione un solo ciclo y un solo trabajador.");
        return;
    }
    openAdjustmentsModal();
});

searchSingleEditBtn?.addEventListener("click", async () => {
    if (currentUser?.role !== "ADMIN" || !isSingleSearchSelection()) return;
    try {
        await openSearchEditModal(selectedSearchCycleIds[0], selectedSearchEmployeeIds[0]);
    } catch (error) {
        alert(error.message);
    }
});

searchSingleAdjustmentsBtn?.addEventListener("click", () => {
    if (currentUser?.role !== "ADMIN" || !isSingleSearchSelection()) return;
    openAdjustmentsModal();
});

searchEditModalCancelBtn?.addEventListener("click", closeSearchEditModal);

searchEditModalSaveBtn?.addEventListener("click", async () => {
    if (!editModalCycleId || !editModalEmployeeId) return;
    const updates = [...searchEditSpreadsheet.querySelectorAll(".cell-input")]
        .map(input => {
            const rowIndex = Number(input.dataset.row);
            const columnIndex = Number(input.dataset.col);
            const row = editModalRows[rowIndex];
            return {
                concept_id: row.conceptId,
                work_date: editModalCycleDate(columnIndex),
                value: input.value === "" ? "0" : input.value,
                changed: Number(input.value || 0) !== Number(row.originalValues[columnIndex] || 0)
            };
        })
        .filter(item => item.changed)
        .map(({concept_id, work_date, value}) => ({concept_id, work_date, value}));

    if (!updates.length) {
        closeSearchEditModal();
        return;
    }

    searchEditModalSaveBtn.disabled = true;
    try {
        const settlement = await apiRequest("/liquidations/cells", {
            method: "POST",
            body: JSON.stringify({
                cycle_id: editModalCycleId,
                employee_id: editModalEmployeeId,
                updates
            })
        });
        const sheetData = settlementToSheetData(settlement, {
            centerLabel: "D&R + Servicios",
            roleLabel: "Consolidado"
        });
        editModalDates = sheetData.dates;
        editModalRows = sheetData.rows;
        renderSearchEditModalSpreadsheet();
        await loadSearchSettlement();
        closeSearchEditModal();
    } catch (error) {
        alert(error.message);
    } finally {
        searchEditModalSaveBtn.disabled = false;
    }
});

spreadsheetSearch.addEventListener("click", async event => {
    const editButton = event.target.closest(".stack-edit-btn");
    if (editButton && currentUser?.role === "ADMIN") {
        try {
            await openSearchEditModal(editButton.dataset.cycleId, editButton.dataset.employeeId);
        } catch (error) {
            alert(error.message);
        }
        return;
    }

    const adjustmentsButton = event.target.closest(".stack-adjustments-btn");
    if (adjustmentsButton && currentUser?.role === "ADMIN") {
        try {
            await focusSearchSettlement(adjustmentsButton.dataset.cycleId, adjustmentsButton.dataset.employeeId);
            openAdjustmentsModal();
        } catch (error) {
            alert(error.message);
        }
    }
});

searchSaveBtn.addEventListener("click", () => modal.classList.remove("hidden"));
cancelSave.addEventListener("click", () => modal.classList.add("hidden"));
searchCancelEditBtn.addEventListener("click", async () => {
    editMode = false;
    searchSaveBtn.classList.add("hidden");
    searchCancelEditBtn.classList.add("hidden");
    searchEditBtn?.classList.toggle("hidden", currentUser?.role !== "ADMIN");
    modal.classList.add("hidden");
    await loadSearchSettlement();
});

confirmSave.addEventListener("click", async () => {
    const updates = [...document.querySelectorAll(".cell-input")]
        .map(input => {
            const rowIndex = Number(input.dataset.row);
            const columnIndex = Number(input.dataset.col);
            const row = rows[rowIndex];
            return {
                concept_id: row.conceptId,
                work_date: settlementCycleDate(columnIndex),
                value: input.value === "" ? "0" : input.value,
                changed: Number(input.value || 0) !== Number(row.originalValues[columnIndex] || 0)
            };
        })
        .filter(item => item.changed)
        .map(({concept_id, work_date, value}) => ({concept_id, work_date, value}));
    if (!updates.length) {
        editMode = false;
        searchSaveBtn.classList.add("hidden");
        searchCancelEditBtn.classList.add("hidden");
        searchEditBtn?.classList.add("hidden");
        modal.classList.add("hidden");
        renderSpreadsheet(activeSheetContainer);
        return;
    }
    confirmSave.disabled = true;
    try {
        const settlement = await apiRequest("/liquidations/cells", {
            method: "POST",
            body: JSON.stringify({
                cycle_id: selectedSearchCycleIds[0],
                employee_id: selectedSearchEmployeeIds[0],
                updates
            })
        });
        editMode = false;
        searchSaveBtn.classList.add("hidden");
        searchCancelEditBtn.classList.add("hidden");
        searchEditBtn?.classList.add("hidden");
        modal.classList.add("hidden");
        applySettlement(settlement);
        if (!adjustmentsModal.classList.contains("hidden")) {
            await loadManualAdjustments();
        }
    } catch (error) {
        alert(error.message);
    } finally {
        confirmSave.disabled = false;
    }
});

adjustmentCloseBtn?.addEventListener("click", closeAdjustmentsModal);
adjustmentNewBtn?.addEventListener("click", () => {
    resetAdjustmentForm();
});

adjustmentsTableBody?.addEventListener("click", event => {
    const editButton = event.target.closest(".adjustment-edit-btn");
    if (editButton) {
        const adjustment = manualAdjustments.find(
            item => item.id === Number(editButton.dataset.adjustmentId)
        );
        if (adjustment) fillAdjustmentForm(adjustment);
    }
});

adjustmentSaveBtn?.addEventListener("click", async () => {
    if (!isSingleSearchSelection()) return;
    const rawUnits = adjustmentUnits.value.trim();
    const rawAmount = adjustmentAmount.value.trim();
    const payload = {
        cycle_id: selectedSearchCycleIds[0],
        employee_id: selectedSearchEmployeeIds[0],
        adjustment_type: adjustmentType.value,
        description: null,
        units: rawUnits === "" ? null : String(Math.round(Number(rawUnits))),
        amount: rawAmount === "" ? "" : String(Math.round(Number(rawAmount))),
        observations: adjustmentObservations.value || null
    };
    if (payload.amount === "") {
        alert("Ingrese un monto.");
        return;
    }
    adjustmentSaveBtn.disabled = true;
    try {
        if (selectedAdjustmentId) {
            await apiRequest(`/manual-adjustments/${selectedAdjustmentId}`, {
                method: "PUT",
                body: JSON.stringify({
                    adjustment_type: payload.adjustment_type,
                    description: payload.description,
                    units: payload.units,
                    amount: payload.amount,
                    observations: payload.observations
                })
            });
        } else {
            await apiRequest("/manual-adjustments", {
                method: "POST",
                body: JSON.stringify(payload)
            });
        }
        await loadManualAdjustments();
        await loadSearchSettlement();
        resetAdjustmentForm();
    } catch (error) {
        alert(error.message);
    } finally {
        adjustmentSaveBtn.disabled = false;
    }
});

adjustmentDeleteBtn?.addEventListener("click", async () => {
    if (!selectedAdjustmentId) return;
    const confirmed = confirm("Se eliminara el ajuste de forma logica. Desea continuar?");
    if (!confirmed) return;
    adjustmentDeleteBtn.disabled = true;
    try {
        await apiRequest(`/manual-adjustments/${selectedAdjustmentId}`, {
            method: "DELETE"
        });
        await loadManualAdjustments();
        await loadSearchSettlement();
        resetAdjustmentForm();
    } catch (error) {
        alert(error.message);
    } finally {
        adjustmentDeleteBtn.disabled = false;
    }
});

newUserBtn.addEventListener("click", () => userForm.classList.remove("hidden"));
cancelUserBtn.addEventListener("click", () => {
    userForm.classList.add("hidden");
    userFullName.value = "";
    userUsername.value = "";
    userPassword.value = "";
    userRole.value = "ADMIN";
    userActive.value = "true";
});
saveUserBtn.addEventListener("click", async () => {
    const payload = {
        full_name: userFullName.value.trim(),
        username: userUsername.value.trim(),
        password: userPassword.value,
        role_name: userRole.value,
        active: userActive.value === "true"
    };
    if (!payload.full_name) {
        alert("Ingrese el nombre del usuario.");
        return;
    }
    if (payload.username.length < 3) {
        alert("El usuario debe tener al menos 3 caracteres.");
        return;
    }
    if (payload.password.length < 10) {
        alert("La contraseña debe tener al menos 10 caracteres.");
        return;
    }
    saveUserBtn.disabled = true;
    try {
        await apiRequest("/users", {
            method: "POST",
            body: JSON.stringify(payload)
        });
        userFullName.value = "";
        userUsername.value = "";
        userPassword.value = "";
        userRole.value = "ADMIN";
        userActive.value = "true";
        userForm.classList.add("hidden");
        await loadUsers();
    } catch (error) {
        alert(error.message);
    } finally {
        saveUserBtn.disabled = false;
    }
});
drImportBtn.addEventListener("click", () =>
    runImport("DR", drImportFile, drImportBtn)
);
servicesImportBtn.addEventListener("click", () =>
    runImport("SERVICES", servicesImportFile, servicesImportBtn)
);
drImportFile.addEventListener("change", () =>
    updateImportSelection(drImportFile, drImportBtn, drImportSelected, "Importar D&R", drImportCard)
);
servicesImportFile.addEventListener("change", () =>
    updateImportSelection(
        servicesImportFile,
        servicesImportBtn,
        servicesImportSelected,
        "Importar Servicios",
        servicesImportCard
    )
);
holidayPrevMonthBtn?.addEventListener("click", () => {
    holidayMonthCursor = new Date(holidayMonthCursor.getFullYear(), holidayMonthCursor.getMonth() - 1, 1);
    loadHolidayCalendar().catch(error => alert(error.message));
});
holidayNextMonthBtn?.addEventListener("click", () => {
    holidayMonthCursor = new Date(holidayMonthCursor.getFullYear(), holidayMonthCursor.getMonth() + 1, 1);
    loadHolidayCalendar().catch(error => alert(error.message));
});
holidayNewBtn?.addEventListener("click", () => {
    if (currentUser?.role !== "ADMIN") {
        alert("Solo ADMIN puede editar feriados.");
        return;
    }
    openHolidayModal({
        holiday_date: toIsoDate(new Date(holidayMonthCursor.getFullYear(), holidayMonthCursor.getMonth(), 1))
    });
});
holidayCalendar?.addEventListener("click", event => {
    const dayButton = event.target.closest("[data-holiday-date]");
    if (!dayButton || currentUser?.role !== "ADMIN") return;
    const editableHoliday = holidayEntries.find(item =>
        item.holiday_date === dayButton.dataset.holidayDate && item.editable
    );
    if (editableHoliday) {
        openHolidayModal(editableHoliday);
        return;
    }
    openHolidayModal({
        holiday_date: dayButton.dataset.holidayDate
    });
});
holidayCancelBtn?.addEventListener("click", closeHolidayModal);
holidaySaveBtn?.addEventListener("click", async () => {
    if (currentUser?.role !== "ADMIN") return;
    const payload = {
        holiday_date: holidayDateInput.value,
        holiday_name: holidayNameInput.value.trim(),
        holiday_scope: "CUSTOM",
        active: holidayActiveInput.checked
    };
    if (!payload.holiday_date || !payload.holiday_name) {
        alert("Ingrese fecha y nombre del feriado.");
        return;
    }
    holidaySaveBtn.disabled = true;
    try {
        if (editingHolidayId) {
            await apiRequest(`/holidays/${editingHolidayId}`, {
                method: "PUT",
                body: JSON.stringify(payload)
            });
        } else {
            await apiRequest("/holidays", {
                method: "POST",
                body: JSON.stringify(payload)
            });
        }
        closeHolidayModal();
        await loadHolidayCalendar();
        await refreshDisplayedSettlementsForHolidayChange();
    } catch (error) {
        alert(error.message);
    } finally {
        holidaySaveBtn.disabled = false;
    }
});

statusCloseBtn?.addEventListener("click", () => {
    hideStatusModal();
});
liquidationCycle.addEventListener("change", () => {
    settlementCycleName.textContent =
        liquidationCycle.options[liquidationCycle.selectedIndex]?.textContent || "";
    loadSettlementEmployees().catch(error => alert(error.message));
});
liquidationEmployee.addEventListener("change", () =>
    loadSettlement().catch(error => alert(error.message))
);
searchBtn.addEventListener("click", async () => {
    if (!selectedSearchCycleIds.length || !selectedSearchEmployeeIds.length) {
        alert("Seleccione al menos un ciclo y un trabajador.");
        return;
    }
    try {
        await loadSearchSettlement();
        return;
    } catch (error) {
        alert(error.message);
    }
});

searchCycleSummary.addEventListener("click", event => {
    event.stopPropagation();
    toggleSearchDropdown(searchCycle, searchCycleSummary);
});

searchEmployeeSummary.addEventListener("click", event => {
    event.stopPropagation();
    toggleSearchDropdown(searchEmployee, searchEmployeeSummary);
});

searchCycle.addEventListener("input", event => {
    if (!event.target.matches("input[data-cycle-id]")) return;
    if (!adjustmentsModal.classList.contains("hidden")) closeAdjustmentsModal();
    selectedSearchCycleIds = checkedValues(searchCycle, "cycleId");
    renderSearchCycleChecklist();
    loadSearchEmployees().catch(error => alert(error.message));
});

searchEmployee.addEventListener("input", event => {
    if (event.target.matches("input[data-select-all-employees]")) {
        const employees = [...searchEmployee.querySelectorAll("input[data-employee-id]")].map(input => ({
            id: Number(input.dataset.employeeId),
            employee_name: input.dataset.employeeName || ""
        }));
        selectedSearchEmployeeIds = event.target.checked ? employees.map(employee => employee.id) : [];
        renderSearchEmployeeChecklist(employees);
        updateSearchActionState();
        if (currentView === "search") {
            searchResultTitle.textContent = "Liquidacion";
            clearSettlement();
        }
        return;
    }
    if (!event.target.matches("input[data-employee-id]")) return;
    if (!adjustmentsModal.classList.contains("hidden")) closeAdjustmentsModal();
    selectedSearchEmployeeIds = checkedValues(searchEmployee, "employeeId");
    renderSearchEmployeeChecklist(
        [...searchEmployee.querySelectorAll("input[data-employee-id]")].map(input => ({
            id: Number(input.dataset.employeeId),
            employee_name: input.dataset.employeeName || ""
        }))
    );
    updateSearchActionState();
    if (currentView === "search") {
        searchResultTitle.textContent = "Liquidacion";
        clearSettlement();
    }
});

searchCycle.addEventListener("click", event => {
    event.stopPropagation();
});

searchEmployee.addEventListener("click", event => {
    event.stopPropagation();
});

document.addEventListener("click", () => {
    closeSearchDropdowns();
});

window.addEventListener("resize", () => {
    if (!searchCycle.classList.contains("hidden")) {
        positionSearchDropdown(searchCycle, searchCycleSummary);
    }
    if (!searchEmployee.classList.contains("hidden")) {
        positionSearchDropdown(searchEmployee, searchEmployeeSummary);
    }
});

window.addEventListener("scroll", () => {
    if (!searchCycle.classList.contains("hidden")) {
        positionSearchDropdown(searchCycle, searchCycleSummary);
    }
    if (!searchEmployee.classList.contains("hidden")) {
        positionSearchDropdown(searchEmployee, searchEmployeeSummary);
    }
}, true);

ratesCycle.addEventListener("change", () => {
    if (currentView === "rates") {
        loadRates().catch(error => alert(error.message));
    }
});

ratesTabs.addEventListener("click", event => {
    const button = event.target.closest("[data-rates-context]");
    if (!button) return;
    currentRatesContext = button.dataset.ratesContext;
    ratesTabs.querySelectorAll(".context-tab").forEach(item =>
        item.classList.toggle("active", item === button)
    );
    loadRates().catch(error => alert(error.message));
});

ratesTableBody.addEventListener("click", event => {
    const button = event.target.closest(".edit-rate-btn");
    if (!button || currentUser?.role !== "ADMIN") return;
    openRateModal({
        rate_id: button.dataset.rateId ? Number(button.dataset.rateId) : null,
        concept_id: Number(button.dataset.conceptId),
        concept_name: button.dataset.conceptName,
        amount: button.dataset.amount === "" ? null : Number(button.dataset.amount)
    });
});

rateCancelBtn.addEventListener("click", closeRateModal);

rateSaveBtn.addEventListener("click", async () => {
    if (!currentRateRow) return;
    const ctx = rateContexts[currentRatesContext];
    const amount = rateModalAmount.value;
    if (amount === "") {
        alert("Ingrese una tarifa.");
        return;
    }
    const confirmed = confirm(
        `Se actualizara ${currentRateRow.concept_name} desde ${cycleNameById(rateModalCycle.value)}. Desea continuar?`
    );
    if (!confirmed) return;
    rateSaveBtn.disabled = true;
    try {
        const payload = {
            cycle_id: Number(rateModalCycle.value),
            amount,
            contract_type: ctx.contractType,
            apply_mode: selectedRateApplyMode()
        };
        if (currentRateRow.rate_id) {
            await apiRequest(`/rates/${currentRateRow.rate_id}`, {
                method: "PUT",
                body: JSON.stringify(payload)
            });
        } else {
            await apiRequest("/rates", {
                method: "POST",
                body: JSON.stringify({
                    concept_id: currentRateRow.concept_id,
                    ...payload
                })
            });
        }
        closeRateModal();
        await loadRates();
        await refreshSettlementIfNeeded(
            ctx.costCenter,
            ctx.roleType,
            Number(rateModalCycle.value)
        );
    } catch (error) {
        alert(error.message);
    } finally {
        rateSaveBtn.disabled = false;
    }
});

newWorkerBtn?.addEventListener("click", () => {
    if (currentUser?.role !== "ADMIN") return;
    resetWorkerForm();
    openWorkerModal();
});

cancelWorkerBtn?.addEventListener("click", resetWorkerForm);

workersTableBody?.addEventListener("click", event => {
    const button = event.target.closest(".edit-worker-btn");
    if (button && currentUser?.role === "ADMIN") {
        editingWorkerId = Number(button.dataset.workerId);
        openWorkerModal({
            name: button.dataset.workerName || "",
            contractType: button.dataset.contractType || "",
            rut: button.dataset.workerRut || "",
            email: button.dataset.workerEmail || "",
            cargo: button.dataset.workerCargo || "",
            readOnlyName: true
        });
        loadWorkers().catch(error => alert(error.message));
        return;
    }
    const deleteButton = event.target.closest(".delete-worker-btn");
    if (deleteButton && currentUser?.role === "ADMIN") {
        const workerId = Number(deleteButton.dataset.workerId);
        const workerName = deleteButton.dataset.workerName || "este trabajador";
        if (!confirm(`¿Eliminar a ${workerName}?`)) {
            return;
        }
        apiRequest(`/workers/${workerId}`, {
            method: "DELETE"
        }).then(async () => {
            if (editingWorkerId === workerId) {
                editingWorkerId = null;
            }
            await refreshAfterWorkerContractChange();
        }).catch(error => alert(error.message));
        return;
    }
    const chooseButton = event.target.closest(".choose-worker-contract-btn");
    if (chooseButton && currentUser?.role === "ADMIN") {
        const workerId = Number(chooseButton.dataset.workerId);
        const contractType = chooseButton.dataset.contractType;
        apiRequest(`/workers/${workerId}`, {
            method: "PUT",
            body: JSON.stringify({ contract_type: contractType })
        }).then(async () => {
            editingWorkerId = null;
            await refreshAfterWorkerContractChange();
        }).catch(error => alert(error.message));
        return;
    }
    const cancelButton = event.target.closest(".cancel-worker-inline-btn");
    if (cancelButton && currentUser?.role === "ADMIN") {
        editingWorkerId = null;
        loadWorkers().catch(error => alert(error.message));
    }
});

saveWorkerBtn?.addEventListener("click", async () => {
    if (currentUser?.role !== "ADMIN") return;
    saveWorkerBtn.disabled = true;
    try {
        const payload = {
            employee_name: workerName.value,
            contract_type: workerContract.value || null,
            rut: workerRut.value || null,
            email: workerEmail.value || null,
            cargo: workerCargo.value || null
        };
        if (editingWorkerId) {
            await apiRequest(`/workers/${editingWorkerId}`, {
                method: "PUT",
                body: JSON.stringify({
                    contract_type: payload.contract_type,
                    rut: payload.rut,
                    email: payload.email,
                    cargo: payload.cargo
                })
            });
        } else {
            await apiRequest("/workers", {
                method: "POST",
                body: JSON.stringify(payload)
            });
        }
        resetWorkerForm();
        await refreshAfterWorkerContractChange();
    } catch (error) {
        alert(error.message);
    } finally {
        saveWorkerBtn.disabled = false;
    }
});

searchExportExcelBtn?.addEventListener("click", () => {
    exportSearchSettlement("xlsx").catch(error => alert(error.message));
});

searchExportPdfBtn?.addEventListener("click", () => {
    exportSearchSettlement("pdf").catch(error => alert(error.message));
});

searchEmailBtn?.addEventListener("click", () => {
    pendingFeature("Enviar por Email quedo visible, pero falta configurar la cuenta del cliente y el flujo de envio.");
});

searchSoftlandBtn?.addEventListener("click", () => {
    pendingFeature("Exportar Softland quedo preparado en la interfaz. Falta definir las columnas exactas del archivo.");
});

liquidationExportExcelBtn?.addEventListener("click", () => {
    exportContextSettlement("xlsx").catch(error => alert(error.message));
});

liquidationExportPdfBtn?.addEventListener("click", () => {
    exportContextSettlement("pdf").catch(error => alert(error.message));
});

liquidationEmailBtn?.addEventListener("click", () => {
    pendingFeature("Enviar por Email quedo visible, pero falta configurar la cuenta del cliente y el flujo de envio.");
});

liquidationSoftlandBtn?.addEventListener("click", () => {
    pendingFeature("Exportar Softland quedo preparado en la interfaz. Falta definir las columnas exactas del archivo.");
});

const existingToken = localStorage.getItem("payroll_access_token");
if (existingToken) {
    apiRequest("/auth/me").then(user => {
        openSession(user);
        Promise.all([loadDashboard(), loadCycleDropdowns()]).then(() => {
            setView("dashboard");
        }).catch(error => alert(error.message));
    }).catch(closeSession);
}

initializeRememberedLogin();
updateImportSelection(drImportFile, drImportBtn, drImportSelected, "Importar D&R", drImportCard);
updateImportSelection(
    servicesImportFile,
    servicesImportBtn,
    servicesImportSelected,
    "Importar Servicios",
    servicesImportCard
);
updateContextActionState();
renderSpreadsheet(spreadsheet);
renderSpreadsheet(spreadsheetSearch);

