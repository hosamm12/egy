# Deploy FastAPI + PostgreSQL (sample)

Vercel stays the Next.js frontend.
This file is the editable backend sample. FastAPI does **not** run on Vercel.

## 1. Render (recommended sample)

1. Open [Render Blueprint](https://dashboard.render.com/blueprints).
2. Connect `hosamm12/egy` and select branch `audit/backend-hardening` until PR #16 is approved.
3. Apply `render.yaml`.
4. In the `egy-api` service set:
   - `BACKEND_CORS_ORIGINS` = your Vercel HTTPS origin, example `https://egy-hosams-projects-92d52a96.vercel.app`
   - `ADMIN_EMAIL` and `ADMIN_PASSWORD` (dashboard only, never git)
5. Wait until the service is live.
6. Copy the public URL only, example `https://egy-api.onrender.com`.
7. In Vercel project `egy` set `NEXT_PUBLIC_API_URL` to that HTTPS URL.
8. Send the URL for `/health/live` and `/health/ready` checks. Do not merge first.

## 2. What you can edit

| File | Change |
| --- | --- |
| `render.yaml` | service name, plan, env keys |
| `BACKEND_CORS_ORIGINS` | frontend origin |
| `apps/backend/app/api/routes/` | API behavior |
| Vercel `NEXT_PUBLIC_API_URL` | frontend → API |

## 3. Security rules

- No secrets in git
- HTTPS only
- Postgres from the provider, not from Vercel
- Alembic runs on boot via `entrypoint.sh`
- Docs stay closed in production (`/docs` disabled when `ENV=production`)
