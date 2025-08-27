#!/usr/bin/env bash
set -e

python -c "from app.scripts.seed_admin import seed; seed()"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
