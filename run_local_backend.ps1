$backendDir = "C:\Users\jtvid\OneDrive\Documentos\Unisan Payroll\backend"
$env:PYTHONPATH = "C:\Users\jtvid\OneDrive\Documentos\Unisan Payroll\backend\.test_deps;C:\Users\jtvid\OneDrive\Documentos\Unisan Payroll\backend"
$env:PAYROLL_DATABASE_URL = "sqlite:///./payroll_dev.db"
$env:PAYROLL_JWT_SECRET = "un-secreto-local-de-al-menos-32-caracteres"
$smtpVariables = @(
    "PAYROLL_SMTP_HOST",
    "PAYROLL_SMTP_PORT",
    "PAYROLL_SMTP_USERNAME",
    "PAYROLL_SMTP_PASSWORD",
    "PAYROLL_SMTP_FROM",
    "PAYROLL_SMTP_TEST_RECIPIENT"
)
foreach ($smtpVariable in $smtpVariables) {
    $smtpValue = [Environment]::GetEnvironmentVariable($smtpVariable, "User")
    if ($smtpValue) {
        Set-Item -Path "Env:$smtpVariable" -Value $smtpValue
    }
}
$localSmtpConfig = Join-Path $backendDir ".smtp.local.ps1"
if (Test-Path $localSmtpConfig) {
    . $localSmtpConfig
}
Set-Location $backendDir
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010
