# 🚀 BackDeck

> **One place to understand what's happening inside your backend.**

BackDeck is a web-based developer workspace that unifies everything a backend developer needs into a single interface — project structure, Docker monitoring, logs, errors, Swagger/OpenAPI, architecture map, and AI-assisted analysis — so you never have to jump between a terminal, Docker Desktop, Swagger, logs, and monitoring tools again.

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
| Python 3.12+ / FastAPI | Microservices framework |
| PostgreSQL + SQLAlchemy 2.0 + Alembic | Data layer (separate DB per service) |
| Redis | Caching, rate limiting, WebSocket state |
| Kafka | Event-driven communication |
| WebSocket | Real-time updates |
| Prometheus + Grafana | Metrics & dashboards |
| Docker / Docker Compose | Containerization & orchestration |
| GitHub Actions | CI/CD |

### Frontend
| Technology | Purpose |
|---|---|
| React + Vite | Web SPA |
| JavaScript | Frontend language |

### AI
| Technology | Purpose |
|---|---|
| Google Gemini Flash API | Fast code/error analysis (Advanced tier planned) |

---

## 🏗 Architecture

BackDeck follows a **microservice architecture** in a **monorepo**. Each service owns its database and communicates through defined interfaces.

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
backdeck/
├── services/
│   ├── gateway/          # API Gateway (routing, JWT, Swagger proxy)
│   ├── auth/             # Auth Service (email/password, GitHub, Google)
│   ├── project/          # Project Service (projects, files, errors, events)
│   ├── analytics/        # Analytics Service (event consumption, metrics)
│   ├── code_analyzer/    # Code Analyzer (AI analysis)
│   └── discovery/        # Discovery Service (service registry)
├── frontend/             # React + Vite SPA
├── libs/                 # Shared libraries (config, async DB, JWT)
├── deploy/               # Docker Compose, Nginx, CI/CD configs
└── docs/                 # Project documentation
```

Every service follows the same isolated layout:

```
services/gateway/
├── app/
│   └── main.py          # FastAPI application + /health endpoint
├── requirements.txt     # Service-only dependencies
└── Dockerfile           # Service-only image
```

---

## 🗺 Roadmap (MVP · ~16 weeks)

| Milestone | Scope | Weeks |
|---|---|---|
| **MS1 — Foundation** | Monorepo, 6 service skeletons, docker-compose, CI, Auth (email + GitHub + Google OAuth) | 1–2 |
| **MS2 — Core Services** | Gateway, Project Service, Workspace Connect CLI | 3–5 |
| **MS3 — Live + UI** | WebSocket hub, Dashboard, tree, file viewer, Swagger, errors, notifications | 6–8 |
| **MS4 — Deployment** | VPS: docker-compose.prod, Nginx, SSL, backups | 9 |
| **MS5 — AI** | Gemini integration, error/file analysis, AI interface | 10–11 |
| **MS6 — Redis + Kafka** | Rate limiting, WS-state, event-driven communication | 12–13 |
| **MS7 — Monitoring + Map** | Prometheus/Grafana, architecture map | 14–15 |
| **MS8 — Final** | E2E verification, production deploy, docs | 16 |

*Beyond MVP: billing & subscriptions, Git-based connection, PR/commit analysis, external notifications, self-hosted, i18n.*

---

## 📊 Project Status

**Early development — building the MVP foundation.**

- ✅ Repository & licensing
- ✅ Architecture and 16-week roadmap finalized
- 🚧 In progress: monorepo skeleton, service scaffolding
- ⏳ Planned: see [Roadmap](#-roadmap-mvp--16-weeks)

---

## 🚀 Getting Started

> Development setup guide will be added as the project evolves (week 1–2: monorepo skeleton + docker-compose.dev).

---

## 📄 License

**View-Only License** — Copyright © 2026 Denis Mishchenko.

This repository is publicly available for **viewing and evaluation purposes only**. You may view and study the code, but you may **not** copy, modify, use, or redistribute it in any form without explicit written permission.

---

*BackDeck — one place to understand what's happening inside your backend.*
