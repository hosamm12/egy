# Backend audit — hosamm12/egy

Branch: `audit/backend-hardening` (do not merge without review).

## Architecture
Frontend Next.js → FastAPI (`/auth` and `/api/v1/*`) → PostgreSQL.
Redis/Celery and `apps/agents` remain demo services. No trip/booking domain exists in the frontend, so none was invented.

Deployment: Docker Compose / GHCR image build. FastAPI is **not** a Vercel app in this repo.

## Implemented in this branch
- JWT subject is user id; inactive users blocked
- Password strength (10+ chars, letter + number)
- Login rate limit per IP
- CORS methods/headers allowlist
- Request ID + security headers + safe 500 body
- `/health/live` and `/health/ready`
- `/files/sample` requires auth + path confinement
- Alembic migration `0001_users`
- `create_all` only outside production
- Admin seed requires `ADMIN_PASSWORD` env (no hardcoded `admin123`)
- Pytest auth/files/health coverage
- GitHub Actions `backend-ci.yml`

## Remaining (manual)
- Rotate `SECRET_KEY` and DB password in every deployed environment
- Run `alembic upgrade head` on Postgres before production
- Add refresh tokens / revocation store if sessions must last beyond 15 minutes
- Booking domain only when the product UI needs it
- Agents still demo; do not grant them DB write credentials
