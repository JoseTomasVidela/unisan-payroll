@echo off
setlocal

set "ROOT=C:\Users\jtvid\OneDrive\Documentos\Unisan Payroll"
set "BACKEND_DIR=%ROOT%\backend"
set "FRONTEND_DIR=%ROOT%\frontend\working_ui"
set "BACKEND_SCRIPT=%BACKEND_DIR%\run_local_backend.ps1"
set "FRONTEND_SCRIPT=%ROOT%\run_local_frontend.ps1"

echo Cerrando instancias previas...
powershell -NoProfile -Command "$ports = 8010,5500; foreach ($port in $ports) { $listeners = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue; if ($listeners) { $listeners | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { try { Stop-Process -Id $_ -Force -ErrorAction Stop; Write-Host ('Puerto ' + $port + ' liberado. Proceso detenido: ' + $_) } catch { Write-Warning ('No fue posible detener el proceso ' + $_ + ' en el puerto ' + $port + '.') } } } }"

timeout /t 2 /nobreak >nul

echo Levantando backend...
start "UNISAN Backend" powershell -NoExit -ExecutionPolicy Bypass -File "%BACKEND_SCRIPT%"

echo Levantando frontend...
start "UNISAN Frontend" powershell -NoExit -ExecutionPolicy Bypass -File "%FRONTEND_SCRIPT%"

timeout /t 4 /nobreak >nul
start "" http://127.0.0.1:5500

echo Aplicacion iniciada.
endlocal
