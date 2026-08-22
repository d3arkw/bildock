# 🚀 Bildock

> **One place to understand what's happening inside your backend.**

Bildock is a web-based developer workspace that unifies everything a backend developer needs into a single interface — project structure, Docker monitoring, logs, errors, Swagger/OpenAPI, architecture map, and AI-assisted analysis — so you never have to jump between a terminal, Docker Desktop, Swagger, logs, and monitoring tools again.

---

## ✨ Key Features

| Area | What it does |
|---|---|
| 🖥 **Workspace Connect** | Lightweight local CLI connector that watches your project, collects Docker state, logs and errors, and streams it to your workspace |
| 📊 **Live Monitoring** | Real-time CPU, RAM, health, ports and status of every Docker container (update interval ~5s) |
| ⚡ **Live Updates** | WebSocket-powered dashboard that updates in real time |
| 🗂 **Project Tree & File Viewer** | Browse project structure and view source files right in the browser |
| 📜 **Swagger / OpenAPI** | Access each service's API docs through the Gateway |
| 🐞 **Error System** | Errors tracked with states (NEW / ACTIVE / RESOLVED), severity, file, line, and history |
| 🔔 **Notifications** | In-workspace alerts: critical errors, unhealthy containers, potential bugs |
| 🤖 **AI Analysis** | Gemini-powered review of errors and files → file, line, description, recommendation |
| 🗺 **Architecture Map** | Auto-generated service map from docker-compose and HTTP calls |
| 💳 **SaaS-ready** | Data model designed for Free / Pro / Team plans from day one |

---

## 🛠 Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python 3.13+ / FastAPI | Microservices framework |
| PostgreSQL + SQLAlchemy 2.0 (async) + Alembic | Data layer, separate DB per service, migrations |
| Redis | Caching, rate limiting, WebSocket state (planned) |
| Kafka | Event-driven communication (planned) |
| WebSocket | Real-time updates (planned) |
| Prometheus + Grafana | Metrics & dashboards (planned) |
| Docker / Docker Compose | Containerization & local development |
| uv | Fast Python package & workspace manager |
| ruff + pytest | Linting, formatting, testing |
| GitHub Actions | CI (lint + format + tests on every PR) |

### Frontend
| Technology | Purpose |
|---|---|
| React + Vite | Web SPA (planned) |

### AI
| Technology | Purpose |
|---|---|
| Google Gemini Flash API | Fast code/error analysis (planned) |

---

## 🏗 Architecture

Bildock follows a **microservice architecture** in a **monorepo (uv workspace)**. Each service owns its database and communicates through defined interfaces.

```
┌──────────────────────────────────────────────────────────┐
│                      Browser (React SPA)                 │
└──────────────────────────┬───────────────────────────────┘
                           │ HTTPS
┌──────────────────────────▼───────────────────────────────┐
│                        Nginx (TLS, static)               │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│                    API Gateway                           │
│        routing · JWT auth · Swagger proxy                │
└──┬─────────────┬──────────────┬──────────────┬───────────┘
   │             │              │              │
┌──▼──────┐ ┌────▼─────┐ ┌──────▼─────┐ ┌──────▼───────┐
│ Auth    │ │ Project  │ │ Analytics  │ │ Code        │
│ Service │ │ Service  │ │ Service    │ │ Analyzer    │
└──┬──────┘ └────┬─────┘ └──────┬─────┘ └──────┬───────┘
   │             │              │              │
   └─────────────┴──────┬───────┴──────────────┘
                        │
            ┌───────────▼───────────┐
            │   Discovery Service   │
            └───────────┬───────────┘
                        │
            ┌───────────▼───────────┐
            │  PostgreSQL (per-svc) │
            │  Redis · Kafka        │
            └───────────────────────┘

┌──────────────────────────────────────────────────────────┐
│   Workspace Connect (CLI, runs on the developer's PC)    │
│   Docker stats · logs · error parsing · state streaming  │
└──────────────────────────────────────────────────────────┘
```

**Key principles:**
- 🔒 **Your code stays yours** — source code is processed locally, only necessary data is sent to the backend.
- 🧩 Each microservice owns its own database.
- 🤝 AI is an assistant that explains and suggests — it never modifies your code.

---

## 📁 Repository Structure

```
bildock/
├── services/               # microservices (each with its own DB)
│   ├── gateway/            # API Gateway (routing, JWT, Swagger proxy)
│   ├── auth/               # Auth Service (email/password, GitHub, Google)
│   │   ├── app/            # application code + User model
│   │   └── migrations/     # Alembic migrations
│   ├── project/            # Project Service (planned)
│   ├── analytics/          # Analytics Service (planned)
│   ├── code_analyzer/      # Code Analyzer (planned)
│   └── discovery/          # Discovery Service (planned)
├── libs/
│   └── bildock-lib/        # shared library: config, database, security, exceptions
├── frontend/               # React + Vite SPA (planned)
├── deploy/                 # deployment configs (planned)
├── docs/                   # project documentation
├── .github/workflows/ci.yml# CI: ruff + format + pytest on every PR
├── docker-compose.yml      # local dev: postgres, redis, kafka, 6 services
├── pyproject.toml          # uv workspace root
├── ruff.toml               # linter configuration
└── .env.example            # environment template
```

Every service follows the same isolated layout:

```
services/<name>/
├── app/                    # FastAPI application
├── migrations/             # Alembic migrations (per service DB)
└── Dockerfile
```

---

## 🚀 Getting Started

Requirements: Docker, uv.

```bash
# 1. Start infrastructure (PostgreSQL, Redis, Kafka)
docker compose up -d

# 2. Install dependencies (uv workspace, all packages)
uv sync --all-packages

# 3. Run migrations (per service)
cd services/auth && alembic upgrade head

# 4. Run checks locally
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

> Note: local PostgreSQL on the host occupies port 5432, so the container exposes 5433. Inside the docker network services use `postgres:5432`.

---

## 🔄 Development Workflow

Every task is developed on a separate branch and merged via Pull Request:

```bash
git checkout -b feat/<issue-number>-<name>
# ... work ...
git add . && git commit -m "feat: ..."
git push -u origin feat/<branch>
gh pr create --title "..." --body "Closes #<issue>"
# CI runs automatically (ruff + format + pytest) — green required
gh pr merge --merge
```

CI protects `main`: no broken code gets merged.

---

## 🗺 Roadmap (MVP · ~16 weeks)

| Milestone | Scope | Status |
|---|---|---|
| **MS1 — Foundation** | Monorepo, service skeletons, docker-compose, shared library, Alembic, CI, Auth | 🚧 In progress — Auth #7 done, #8 in work (refresh + logout) |
| **MS2 — Core Services** | Gateway, Project Service, Workspace Connect CLI | ⏳ |
| **MS3 — Live + UI** | WebSocket hub, Dashboard, tree, file viewer, Swagger, errors, notifications | ⏳ |
| **MS4 — Deployment** | VPS: docker-compose.prod, Nginx, SSL, backups | ⏳ |
| **MS5 — AI** | Gemini integration, error/file analysis, AI interface | ⏳ |
| **MS6 — Redis + Kafka** | Rate limiting, WS-state, event-driven communication | ⏳ |
| **MS7 — Monitoring + Map** | Prometheus/Grafana, architecture map | ⏳ |
| **MS8 — Final** | E2E verification, production deploy, docs | ⏳ |

*Beyond MVP: billing & subscriptions, Git-based connection, PR/commit analysis, external notifications, self-hosted, i18n.*

---

## 📄 License

**View-Only License** — Copyright © 2026 Denis Mishchenko.

This repository is publicly available for **viewing and evaluation purposes only**. You may view and study the code, but you may **not** copy, modify, use, or redistribute it in any form without explicit written permission.

---

*Bildock — one place to understand what's happening inside your backend.*
