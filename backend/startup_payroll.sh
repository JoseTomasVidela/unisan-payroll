#!/bin/sh
set -eu

PORT_TO_USE="${PORT:-8000}"

if [ -f "/home/site/wwwroot/antenv/bin/activate" ]; then
  . /home/site/wwwroot/antenv/bin/activate
elif [ -f "../antenv/bin/activate" ]; then
  . ../antenv/bin/activate
fi

exec gunicorn \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers "${PAYROLL_GUNICORN_WORKERS:-2}" \
  --timeout "${PAYROLL_GUNICORN_TIMEOUT:-120}" \
  --bind "0.0.0.0:${PORT_TO_USE}" \
  app.main:app
