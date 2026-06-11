@echo off
set PYTHONPATH=C:\Users\jtvid\OneDrive\Documentos\Unisan Payroll\backend\.test_deps;C:\Users\jtvid\OneDrive\Documentos\Unisan Payroll\backend
set PAYROLL_DATABASE_URL=sqlite:///./payroll_dev.db
set PAYROLL_JWT_SECRET=un-secreto-local-de-al-menos-32-caracteres
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010
