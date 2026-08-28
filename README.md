# Civic Resolution (working name)

**Independent hackathon prototype — not an official government product.** Built for
"Build What Moves India." All government interactions, authorities, case data, officer
names, and SLAs shown in this prototype are **simulated/synthetic**. No real government
systems are accessed, scraped, or integrated with.

## What this is

Citizens shouldn't have to know which department, portal, or form handles their problem.
This prototype lets a citizen describe a problem in plain language; the system:

1. Understands the problem (AI).
2. Figures out which (mock) government authority is responsible.
3. Creates a trackable case with a plain-language explanation of what's happening.
4. Tracks delay against a simulated SLA and supports escalation.
5. Requires the **citizen** to verify a case marked "resolved" before it's actually closed —
   reopening it if they say it isn't fixed.

See `MASTER_BUILD_CONTEXT` in the project history for the full product spec.

## Project structure

```
backend/    FastAPI app (AI orchestration, mock government registry, case logic)
frontend/   React + Vite + TypeScript + Tailwind (citizen-facing UI)
```

## Running locally

### Backend

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate      # Windows; use .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
cp .env.example .env        # fill in OPENAI_API_KEY / SUPABASE_* if you have them — both are optional
uvicorn app.main:app --reload --port 8000
```

Demo data seeds automatically on startup. Run tests with `pytest` from `backend/`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env        # defaults to http://localhost:8000
npm run dev
```

Open the printed local URL. Pick a demo persona (no real login) and try:
> "The streetlight outside my house hasn't worked for two weeks."

### Hidden demo-only route

`/admin` simulates a government official marking a case resolved — it's not linked from
the app's navigation and exists only so the resolution-verification loop can be demoed live.

## AI and data modes (fallback-first by design)

The backend works fully **without** any API key or database credentials:

- **AI**: if `OPENAI_API_KEY` is set, problem understanding / evidence interpretation /
  safety screening call OpenAI with structured outputs. If it's absent (or a call fails),
  a deterministic rule-based fallback produces the same shape of response. Every AI output
  carries `source: "openai" | "fallback"` so this is never hidden.
- **Storage**: if `SUPABASE_URL` is set, the backend persists to Supabase Postgres. If not,
  it uses an in-memory store seeded with the same demo data. Routers/services depend only
  on an abstract `Repository` interface — swapping backends requires no business-logic changes.

Check `GET /api/health` to see which mode is currently active.

## Demo scenarios (seeded on startup)

| Case | Domain | Notes |
|---|---|---|
| `CIV-20481` | Streetlight outage | Hero scenario — overdue, ready to escalate/resolve/verify live |
| `PF-28491` | EPFO PF claim rejection | Pre-escalated, blocked on employer verification |
| `SCH-31007` | Scholarship payment delay | |
| `PEN-44210` | Pension delay | Heavily overdue |
| `CERT-55019` | Certificate application delay | Stuck at field verification |

## Deployment

- **Frontend**: Vercel. `frontend/vercel.json` sets the build/output config. Set
  `VITE_API_BASE_URL` in the Vercel project to the deployed backend URL.
- **Backend**: Render. `backend/render.yaml` defines the service. Set `OPENAI_API_KEY`
  (optional), `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` / `SUPABASE_ANON_KEY` (optional),
  and `CORS_ALLOW_ORIGINS` to the deployed Vercel domain.

## What's simulated

Everything government-side: authorities, departments, officer names/roles, SLAs, case
timelines, escalation submissions, and resolution events. No real Aadhaar, PAN, OTP,
payments, or government credentials are used or requested anywhere in this prototype.
