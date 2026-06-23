$workspaceRoot = "C:\Users\jtvid\OneDrive\Documentos\Unisan Payroll"
$backendDir = Join-Path $workspaceRoot "backend"
$frontendDir = Join-Path $workspaceRoot "frontend\working_ui"
$backendScript = Join-Path $workspaceRoot "run_local_backend.ps1"
$frontendScript = Join-Path $workspaceRoot "run_local_frontend.ps1"
$backendPort = 8010
$frontendPort = 5500

function Stop-PortProcess {
    param(
        [int]$Port
    )

    $listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if (-not $listeners) {
        return
    }

    $processIds = $listeners | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($processId in $processIds) {
        try {
            Stop-Process -Id $processId -Force -ErrorAction Stop
            Write-Host "Puerto $Port liberado. Proceso detenido: $processId"
        } catch {
            Write-Warning "No fue posible detener el proceso $processId en el puerto $Port."
        }
    }
}

Write-Host "Cerrando instancias previas..."
Stop-PortProcess -Port $backendPort
Stop-PortProcess -Port $frontendPort
Start-Sleep -Seconds 2

Write-Host "Levantando backend..."
Start-Process -FilePath "powershell.exe" `
    -ArgumentList @(
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-File", $backendScript
    ) `
    -WorkingDirectory $backendDir `
    -WindowStyle Minimized

Write-Host "Levantando frontend..."
Start-Process -FilePath "powershell.exe" `
    -ArgumentList @(
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-File", $frontendScript
    ) `
    -WorkingDirectory $frontendDir `
    -WindowStyle Minimized

Write-Host "Esperando inicio de servicios..."
Start-Sleep -Seconds 4

try {
    $health = Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:8010/api/health" -TimeoutSec 10
    Write-Host "Backend OK: $($health.Content)"
} catch {
    Write-Warning "Backend no respondió en /api/health."
}

try {
    $front = Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:5500" -TimeoutSec 10
    Write-Host "Frontend OK: HTTP $($front.StatusCode)"
} catch {
    Write-Warning "Frontend no respondió en :5500."
}

Start-Process "http://127.0.0.1:5500"
Write-Host "Aplicación abierta en http://127.0.0.1:5500"
