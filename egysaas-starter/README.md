# EgySaaS Starter (Monorepo)

A production-ready scaffold for **backend (FastAPI)**, **frontend (Next.js)**, **multi-agent orchestration (Python)**,
with **PostgreSQL**, **Redis**, **Celery workers**, and **Docker Compose** for local and cloud deploys.

## What you get
- FastAPI backend with JWT auth, users, and health endpoints
- Next.js 14 (App Router) frontend with login/register and a protected dashboard
- Simple "multi-agent" orchestrator service (HTTP-based demo) that can trigger backend automation
- PostgreSQL + Redis + Celery worker + Celery beat (scheduled jobs)
- One-command local dev via Docker Compose
- GitHub Actions workflow to build container images
- Makefile for common tasks

---

## Quickstart (Local)

1) Copy env:
```bash
cp .env.example .env
```

2) Start everything:
```bash
make up
```

3) Open: 
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

### Default admin (created on first run)
- Email: `admin@example.com`
- Password: `admin123`

---

## Cloud deploy (simple VM + Docker Compose)

1) Push this repo to GitHub.
2) On a Linux VM with Docker installed, clone your repo and copy your `.env`.
3) Run `docker compose -f docker-compose.yml up -d --build`.
4) Point your domain to the VM. (Optional: Add a reverse proxy like Traefik/Nginx + Let's Encrypt).

> For a managed PaaS, build the images using the provided GitHub Actions and deploy to services like
> Fly.io, Render, Railway, or AWS ECS/Fargate. You only need to inject env vars and connect Postgres/Redis.

---

## Services & Ports
- Frontend (Next.js): `3000`
- Backend (FastAPI): `8000`
- Postgres: `5432`
- Redis: `6379`
- Celery worker & beat are internal services

---

## Dev commands

```bash
# Bring stack up / down
make up
make down

# Tail logs
make logs

# Run only the backend locally (without Docker)
cd apps/backend && uvicorn app.main:app --reload --port 8000

# Run Next.js locally (without Docker)
cd apps/frontend && npm i && npm run dev
```

---

## Folder layout

```
egysaas-starter/
  apps/
    backend/       # FastAPI + SQLAlchemy + JWT + Celery
    frontend/      # Next.js 14 + minimal auth pages
    agents/        # Simple "multi-agent" orchestrator demo
  infra/           # (Room for IaC, k8s manifests, etc.)
  scripts/         # Helper scripts
  docker-compose.yml
  Makefile
  .env.example
```

---

## Notes on "Multi-Agent"
The `agents` service demonstrates a lightweight "multi-agent" pattern using plain Python classes to keep
the demo dependency-light. It routes a task between two agents (Planner & Executor) and hits the backend
to simulate work. You can swap this with your favorite framework later (e.g., LangGraph) by adjusting `agents/orchestrator.py`.

Enjoy and build on! 🚀
