# Backend audit — hosamm12/egy

Branch: `audit/backend-hardening` (do not merge without review).

## Architecture
Frontend Next.js → FastAPI (`/auth` and `/api/v1/*`) → PostgreSQL.
Redis/Celery and `apps/agents` remain demo services. No trip/booking domain exists in the frontend, so none was invented.

Deployment: Docker Compose / GHCR image build. FastAPI is **not** hosted as the Vercel runtime.
Vercel project `egy` preview can build Next. That does not prove API or database health.

## Implemented
- JWT subject is user id; inactive users blocked
- Password strength (10+ chars, letter + number)
- Login rate limit per IP
- CORS methods/headers allowlist
- Request ID + security headers + safe 500 body
- `/health/live` and `/health/ready`
- `/files/sample` requires auth + path confinement
- Alembic migration `0001_users`
- `create_all` only outside production
- Admin seed requires `ADMIN_PASSWORD` env
- Deployed frontend no longer silently calls `http://localhost:8000`

## Remaining (manual, pre-merge)
- Deploy FastAPI + PostgreSQL somewhere reachable (not localhost / Compose names)
- Set Vercel `NEXT_PUBLIC_API_URL` to that HTTPS origin (name only in dashboards; do not commit secrets)
- Add the Vercel frontend origin to `BACKEND_CORS_ORIGINS`
- Run `alembic upgrade head` on that Postgres
- Confirm GET `/health/live` and `/health/ready` return 200
- Do not merge PR #16 until Vercel Next.js → FastAPI → PostgreSQL is verified
