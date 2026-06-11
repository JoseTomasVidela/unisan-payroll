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
const modal = document.getElementById("confirm-modal");
const cancelSave = document.getElementById("cancel-save");
const confirmSave = document.getElementById("confirm-save");
const newUserBtn = document.getElementById("new-user-btn");
const cancelUserBtn = document.getElementById("cancel-user-btn");
const userForm = document.getElementById("user-form");

let editMode = false;

const contexts = {
    "dr-drivers": ["Liquidaciones D&R Choferes", "D&R", "Chofer"],
    "dr-assistants": ["Liquidaciones D&R Auxiliares", "D&R", "Auxiliar"],
    "services-drivers": ["Liquidaciones Servicios Choferes", "SERVICES", "Chofer"],
    "services-assistants": ["Liquidaciones Servicios Auxiliares", "SERVICES", "Auxiliar"]
};

const dates = [
    ["22-04","mié","Ok"], ["23-04","jue","Ok"], ["24-04","vie","Ok"], ["25-04","sáb","Ok"],
    ["26-04","dom","Ok"], ["27-04","lun","Ok"], ["28-04","mar","Ok"], ["29-04","mié","Sin Produc"],
    ["30-04","jue","Ok"], ["01-05","vie","Descanso"], ["02-05","sáb","Descanso"], ["03-05","dom","Descanso"],
    ["04-05","lun","Ok"], ["05-05","mar","Libre Compensatorio"], ["06-05","mié","Ok"], ["07-05","jue","Ok"],
    ["08-05","vie","Ok"], ["09-05","sáb","Ok"], ["10-05","dom","Sin Producción"], ["11-05","lun","Ok"],
    ["12-05","mar","Sin Producción"], ["13-05","mié","Ok"], ["14-05","jue","Ok"], ["15-05","vie","Ok"],
    ["16-05","sáb","Libre Compe"], ["17-05","dom","Ok"], ["18-05","lun","Sin Producción"], ["19-05","mar","Libre Compensatorio"],
    ["20-05","mié","Ok"], ["21-05","jue","Ok"]
];

const rows = [
    {label:"Estado", units:"", rate:"", total:"", values:dates.map(d=>d[2]), status:true},
    {label:"Despacho / Retiro", units:372, rate:751, values:[49,40,28,0,0,2,20,28,12,0,0,0,0,0,34,22,26,0,0,0,32,0,6,11,0,0,20,0,42,0]},
    {label:"Entrada < 19:30", units:1, rate:2506, values:[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]},
    {label:"Feria Semana 01", units:6, rate:10025, values:[1,1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]},
    {label:"Feria Semana 02", units:4, rate:12532, values:[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0]},
    {label:"Fuera Radio Normal", units:1, rate:3760, values:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]},
    {label:"Fuera Radio V Región", units:1, rate:6266, values:[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]},
    {label:"Sabado Semana 01", units:2, rate:20051, values:[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]},
    {label:"Domingo Semana 01", units:2, rate:25064, values:[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]},
    {label:"Viajes Por Cliente", units:19, rate:6266, values:[0,0,0,0,5,5,0,0,0,0,0,0,0,0,1,0,0,5,3,0,0,0,0,0,0,0,0,0,0,0]},
    {label:"Sábado > 16:00", units:2, rate:10025, values:[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]},
    {label:"Domingo > 16:00", units:3, rate:11279, values:[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1]},
    {label:"Domingo Semana 02", units:1, rate:28823, values:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]},
    {label:"Secado Fin de Semana", units:18, rate:551, values:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,18]},
    {label:"Evento", units:158, rate:751, values:[0,0,16,0,0,4,0,17,0,0,0,0,1,0,40,40,40,0,0,0,0,0,0,0,0,0,0,0,0,0]},
    {label:"SERVICIOS", section:true},
    {label:"BONO FUERA PRODUCCION", section:true},
    {label:"", empty:true},
    {label:"", empty:true},
    {label:"TOTAL A PAGAR", totalRow:true, totalOverride:822974, values:[51,41,45,7,7,6,21,46,12,0,0,0,2,0,76,63,67,7,5,0,33,0,6,11,0,0,21,0,43,20]},
    {label:"VARIABLE DIARIO", summary:true, values:["###","###","###","###","###","###","###","###","###",0,0,0,"###",0,"###","###","###","###","###",0,"###",0,"###","###",0,0,"###",0,"###","###"]},
    {label:"DIA TRABAJADO [SI=1 ; NO=0]", summary:true, values:[3,1,1,1,1,1,1,1,1,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,1,1]},
    {label:"SEMANA CORRIDA", summary:true, totalOverride:214114, values:["","","","","#","","","","","","###","","","","","","","","###","","","","","","","###","","","###",""]},
    {label:"PRODUCCION TOTAL", summary:true, totalOverride:1037087, values:[]},
    {label:"Bono de Salida", footer:true, units:424721},
    {label:"UNIBOX", footer:true, units:118728},
    {label:"PRODUCCION", footer:true, units:279525}
];

function money(value) {
    if (value === "" || value === undefined || value === null) return "";
    return Number(value).toLocaleString("es-CL");
}

function rowTotal(row) {
    if (row.totalOverride !== undefined) return row.totalOverride;
    if (!row.rate || !row.units) return "";
    return row.units * row.rate;
}

function renderSpreadsheet(container) {
    let html = `<table class="sheet-table"><thead>
        <tr>
            <th class="fixed">Daniel Peña</th>
            <th class="units">Daniel Peña<br>Unidades</th>
            <th class="rate">Cargo</th>
            <th class="total">Chofer<br>Total $</th>
            ${dates.map(d => `<th class="date-head">${d[0]}</th>`).join("")}
        </tr>
        <tr>
            <th class="fixed">Actividad</th>
            <th class="units"></th>
            <th class="rate"></th>
            <th class="total"></th>
            ${dates.map(d => `<th class="date-head">${d[1]}</th>`).join("")}
        </tr>
    </thead><tbody>`;

    rows.forEach((row, rIndex) => {
        if (row.empty) {
            html += `<tr><td class="fixed"></td><td class="units"></td><td class="rate"></td><td class="total"></td>${dates.map(()=>"<td></td>").join("")}</tr>`;
            return;
        }
        const cls = row.section ? "section" : row.totalRow ? "total-row" : row.summary ? "summary-row" : "";
        html += `<tr class="${cls}">
            <td class="fixed ${row.section ? "section" : row.totalRow ? "summary-label" : ""}">${row.label}</td>
            <td class="units">${money(row.units)}</td>
            <td class="rate">${money(row.rate)}</td>
            <td class="total">${money(rowTotal(row))}</td>`;

        dates.forEach((d, cIndex) => {
            const val = row.values ? row.values[cIndex] ?? "" : "";
            const isEditable = editMode && !row.status && !row.section && !row.summary && !row.totalRow && !row.footer;
            const blue = row.status || row.totalRow || row.summary ? "blue" : "";
            if (row.status) {
                html += `<td class="status-head">${val}</td>`;
            } else if (isEditable) {
                html += `<td class="${blue}"><input class="cell-input" value="${val}" data-row="${rIndex}" data-col="${cIndex}"></td>`;
            } else {
                html += `<td class="${blue}">${val}</td>`;
            }
        });
        html += `</tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;
}

function setView(viewId) {
    views.forEach(v => v.classList.remove("active"));
    navItems.forEach(n => n.classList.remove("active"));
    const activeNav = document.querySelector(`[data-view="${viewId}"]`);
    if (activeNav) activeNav.classList.add("active");

    if (viewId === "dashboard") {
        document.getElementById("dashboard").classList.add("active");
        title.textContent = "Dashboard";
        breadcrumb.textContent = "Dashboard";
        return;
    }

    if (viewId === "search") {
        document.getElementById("search").classList.add("active");
        title.textContent = "Búsqueda";
        breadcrumb.textContent = "Búsqueda";
        renderSpreadsheet(spreadsheetSearch);
        return;
    }

    if (viewId === "users") {
        document.getElementById("users").classList.add("active");
        title.textContent = "Usuarios";
        breadcrumb.textContent = "Usuarios";
        return;
    }

    const ctx = contexts[viewId];
    liquidationView.classList.add("active");
    title.textContent = ctx[0];
    breadcrumb.textContent = ctx[0];
    liquidationPanelTitle.textContent = ctx[0];
    document.getElementById("settlement-center").textContent = ctx[1];
    document.getElementById("settlement-role").textContent = ctx[2];
    renderSpreadsheet(spreadsheet);
}

loginBtn.addEventListener("click", () => {
    loginScreen.classList.add("hidden");
    appShell.classList.remove("hidden");
});

logoutBtn.addEventListener("click", () => {
    appShell.classList.add("hidden");
    loginScreen.classList.remove("hidden");
});

toggleSidebar.addEventListener("click", () => {
    appShell.classList.toggle("sidebar-collapsed");
});

navItems.forEach(item => {
    item.addEventListener("click", () => setView(item.dataset.view));
});

editBtn.addEventListener("click", () => {
    editMode = true;
    editBtn.classList.add("hidden");
    saveBtn.classList.remove("hidden");
    renderSpreadsheet(spreadsheet);
});

saveBtn.addEventListener("click", () => modal.classList.remove("hidden"));
cancelSave.addEventListener("click", () => modal.classList.add("hidden"));

confirmSave.addEventListener("click", () => {
    document.querySelectorAll(".cell-input").forEach(input => {
        const r = Number(input.dataset.row);
        const c = Number(input.dataset.col);
        rows[r].values[c] = input.value;
    });
    editMode = false;
    saveBtn.classList.add("hidden");
    editBtn.classList.remove("hidden");
    modal.classList.add("hidden");
    renderSpreadsheet(spreadsheet);
});

newUserBtn.addEventListener("click", () => userForm.classList.remove("hidden"));
cancelUserBtn.addEventListener("click", () => userForm.classList.add("hidden"));

renderSpreadsheet(spreadsheet);
renderSpreadsheet(spreadsheetSearch);
