# Backend audit — hosamm12/egy

Branch: `audit/backend-hardening` (do not merge without review).

## Architecture
Frontend Next.js → FastAPI (`/auth` and `/api/v1/*`) → PostgreSQL.
Redis/Celery and `apps/agents` remain demo services. No trip/booking domain exists in the frontend, so none was invented.

Deployment: Docker Compose / GHCR image build. FastAPI is **not** hosted as the Vercel runtime.
Vercel project `egy` was set to Blitz/Next at the **repo root**, so builds failed with NEXT_NO_VERSION until a root `package.json` + `vercel.json` pointed install/build at `apps/frontend`.
Vercel project `egy-thfd` being READY only means a framework-less empty build succeeded — it is not proof of production API/DB health.

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
- Pytest in `blank.yml` (the workflow that actually runs jobs) and `backend-ci.yml`

## Remaining (manual)
- In Vercel project `egy` set Root Directory to `apps/frontend` and Framework to Next.js
- Rotate `SECRET_KEY` and DB password in every deployed environment
- Run `alembic upgrade head` on Postgres before production
- Add refresh tokens if sessions must last beyond 15 minutes
- Do not treat `egy-thfd` READY as production-ready backend
