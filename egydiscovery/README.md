# EgyDiscovery Suite PRO (Best Mix)

**One command** to run Website + Auth + APIs + DB + n8n:
```bash
cp .env.sample .env
docker compose up -d --build
```
- Frontend: http://localhost:3000
- Backend:  http://localhost:8000  (Docs: /docs)
- n8n:      http://localhost:5678

## What’s inside
- **Frontend (Next.js)**: `/frontend` → login + dashboard to send prompts.
- **Backend (FastAPI)**: `/backend/app` → JWT auth, multi-agent endpoints, data APIs, health.
- **Agents**: simple router + auto use of your `master_controller.py` if provided.
- **Automation (n8n)**: `/n8n/workflows` → master & route webhooks + 5 imported flow(s) as `imported__*.json`.
- **DB/Queue**: Postgres + Redis.
- **Infra**: Docker Compose, `.env.sample`.

## API overview
- `POST /api/v1/auth/register`, `POST /api/v1/auth/login` → JWT
- `POST /api/v1/agents/master` (Bearer token)
- `POST /api/v1/agents/route`  (Bearer token)
- `POST /api/v1/data/leads` | `GET /api/v1/data/leads`
- `GET  /api/v1/health`

## n8n
1. Open http://localhost:5678 (basic auth from `.env`)
2. Import/activate:
   - `n8n/workflows/master_agent_webhook.json`
   - `n8n/workflows/route_agent_webhook.json`
   - any `n8n/workflows/imported__*.json`

### Webhook test
```bash
curl -X POST http://localhost:5678/webhook/master   -H 'Content-Type: application/json'   -d '{"prompt":"Score 5 public leads in Hurghada"}'
```

## Deploy (quick)
- VM with Docker: copy repo, set `.env`, then:
```bash
docker compose up -d --build
```
- Add reverse proxy (Caddy/Traefik/NGINX) for HTTPS + map domains:
  - `https://app.example.com` → frontend (3000)
  - `https://api.example.com` → backend (8000)
  - `https://flow.example.com` → n8n (5678)

## Notes
- For production: secure secrets, enable HTTPS, CORS allow-lists, and add Alembic migrations.
- You can replace the router stubs with real agent logic or your `master_controller.py`.


## NEW: OAuth (Google/Microsoft)
- Set OAuth env vars in `.env`, then rebuild.
- Start OAuth: `GET /api/v1/auth/oauth/google/login` (or `/microsoft/login`)
- After callback, backend redirects to `/oauth-complete#token=...`, which stores JWT and sends you to `/dashboard`.

## NEW: Agents (research/scrape/enrich) + persistence
- Use `params.agent` = `scrape` or `enrich`, or write prompts containing keywords.
- When a result contains `items`, they are auto-saved to `/data/leads` (source=master/router, tag=auto).

## NEW: Outreach (n8n)
- Import `outreach_twilio_whatsapp.json`, `outreach_telegram.json`, `outreach_email.json`
- Set credentials (Twilio, Telegram, SMTP) in n8n and `.env`. Trigger via:
```bash
curl -X POST http://localhost:5678/webhook/lead_outreach_email   -H 'Content-Type: application/json'   -d '{"to":"someone@example.com","subject":"Hello","message":"Hi!"}'
```

## Alembic migrations
```bash
# (in container) run:
alembic -c backend/alembic.ini upgrade head
```

## Production TLS with Caddy
1) Point DNS: `app.example.com`, `api.example.com`, `flow.example.com` to your server
2) Edit `deploy/Caddyfile` (set your email + domains)
3) Run:
```bash
docker compose -f docker-compose.yml -f deploy/docker-compose.caddy.yml up -d --build
```


## Automation rules (n8n)
- **Score ≥ 70** → send **WhatsApp + Email**
- **50 ≤ Score < 70** → send **Email only**
- **VIP tag** (any score) → send **Telegram alert to team**

### Triggers
- **Lead form** (frontend `/lead-form` → backend `/api/v1/events/lead` → n8n `/webhook/lead_ingest`)
- **New lead** (POSTed to `/api/v1/events/lead` from any source)
- **Chatbot open/message** (frontend `/chat` → backend `/api/v1/events/chat` → n8n `/webhook/chat_event`)

### n8n workflows
- `lead_ingest_router.json` — implements the rules above and persists to DB
- `chat_event_router.json` — logs chat events as leads and enriches

### Outreach endpoints (already included)
- WhatsApp: `outreach_twilio_whatsapp.json` — webhook `/webhook/lead_outreach_whatsapp`
- Email: `outreach_email.json` — webhook `/webhook/lead_outreach_email`
- Telegram: `outreach_telegram.json` — webhook `/webhook/lead_outreach_telegram`
