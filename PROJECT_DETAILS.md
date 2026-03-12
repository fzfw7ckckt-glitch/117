# OSINT Platform 2026 — Повні деталі проекту

> Документ зібрано автоматично. Останнє оновлення: березень 2026.

---

## 1. Загальний огляд

**Назва:** OSINT Platform 2026  
**Тип:** Гібридна платформа OSINT-розвідки  
**Ліцензія:** MIT  
**Мова:** Українська / English (UA/EN перемикач в UI)

### Ключові можливості

| Можливість | Опис |
|------------|------|
| **150+ OSINT-інструментів** | Maigret, GeoSpy, Picarta, YouControl, Shodan, Censys, Hunter, HIBP тощо |
| **Асинхронна обробка** | Celery воркери для паралельної розвідки |
| **Юридичні докази** | OpenTimestamps, SHA-256 хеші, timestamp-докази |
| **AI-агенти** | BlacksmithAI, Perplexity, MiniMax |
| **Анонімність** | Tor-інтеграція (SOCKS5 :9050) |
| **Веб-інтерфейс** | Next.js 14, темна тема |
| **Безпека** | JWT-автентифікація, rate-limiting, CORS |

---

## 2. Архітектура

```
┌─────────────────────────────────────────────────────────────┐
│  Nginx (HTTPS Reverse Proxy) — profile prod                  │
│  Port: 80, 443                                               │
└──────────────────────┬─────────────────────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         │                            │
┌────────▼────────┐          ┌────────▼────────┐
│ FastAPI         │          │ Next.js         │
│ :8000           │          │ :3000           │
│ API + CORS      │          │ Dashboard       │
└────────┬────────┘          └─────────────────┘
         │
┌────────▼────────────────────┐
│ Celery Workers              │
│ 4 concurrent tasks          │
│ Chromium + Tor support      │
└────────┬────────────────────┘
         │
┌────────┴────────┬──────────┬──────────┐
▼                 ▼          ▼          ▼
PostgreSQL      Redis       Tor        Chromium
:5432           :6379       :9050       Scraping
```

---

## 3. Структура проекту

```
osint-platform-2026/
├── app/                          # Backend (FastAPI)
│   ├── main.py                   # Entry point, routes, OSINT search
│   ├── config.py                 # Env vars, API keys
│   ├── database.py               # SQLAlchemy session
│   ├── cases_store.py            # InvestigationCase, CaseTimelineEvent
│   ├── models.py                 # Investigation, Evidence (legacy)
│   ├── routers/
│   │   ├── auth.py               # JWT login, refresh
│   │   ├── health.py             # /health
│   │   ├── investigations.py     # CRUD investigations
│   │   └── tools.py              # Tool run, status, catalog
│   ├── tasks/
│   │   ├── celery_app.py         # Celery config
│   │   ├── tools_47.py           # SIGINT, HUMINT, Leaks tasks
│   │   └── integrity.py          # Blockchain timestamps
│   └── utils/
│       ├── sigint_clients.py     # Censys, FOFA, ZoomEye, SecurityTrails, BinaryEdge, CriminalIP, GreyNoise
│       ├── humint_clients.py     # Hunter, SocialLinks, GHunt
│       ├── leaks_clients.py      # HIBP, BreachDirectory, HudsonRock, SpyCloud, IntelligenceX, LeakLookup
│       ├── web_clients.py        # URLScan, Wayback, VirusTotal, Shodan, Netlas, AlienVault, WhoisRDAP, AbuseIPDB
│       ├── hashing.py            # SHA-256
│       └── __init__.py
│
├── web/                          # Frontend (Next.js 14)
│   ├── app/
│   │   ├── layout.tsx            # Root layout, header, nav
│   │   ├── page.tsx              # Home: search, metrics, categories, connected tools
│   │   ├── control/page.tsx       # Tools grid (/control)
│   │   ├── catalog/page.tsx       # Catalog with filters
│   │   ├── tools/page.tsx        # Keys & connections modal
│   │   ├── investigations/page.tsx # Cases list
│   │   └── api/
│   │       └── osint/search/route.ts  # Proxy to backend
│   │       └── cases/            # Cases API proxy
│   ├── components/
│   │   ├── SiteNav.tsx           # Пошук, Інструменти, Каталог, API Docs
│   │   ├── HeaderActions.tsx     # Keys, UA/EN, REBOOT
│   │   ├── ToolCard.tsx, ToolGrid.tsx, ToolModal.tsx
│   │   └── ...
│   ├── context/AppContext.tsx    # lang, userKeys, disabledTools
│   ├── data/
│   │   ├── tools_catalog.ts      # 70+ tools, 12 categories
│   │   └── tools_47.ts           # Connected tools list
│   ├── lib/store.ts
│   ├── app/globals.css           # Dark theme, CSS vars
│   ├── package.json
│   ├── next.config.js
│   └── Dockerfile
│
├── worker/
│   └── Dockerfile                # Celery worker (Chromium, Tor)
│
├── scripts/
│   ├── docker-build.sh
│   ├── health-check.sh
│   └── init_db.sql
│
├── tests/
│   ├── conftest.py
│   └── test_routers.py
│
├── docker-compose.yml            # postgres, redis, tor, api, worker, web, nginx
├── docker-compose.dev.yml        # Hot reload, pgAdmin, Redis Commander
├── Dockerfile.api                # FastAPI multi-stage
├── requirements.txt              # Full Python deps
├── requirements-api.txt          # Lightweight API deps
├── requirements-worker.txt       # Worker deps
├── .env.example
├── nginx.conf
├── railway.toml                  # Railway build config
├── Makefile
└── .github/workflows/ci-cd.yml   # CI/CD pipeline
```

---

## 4. Технологічний стек

### Backend

| Компонент | Версія / Технологія |
|-----------|---------------------|
| Runtime | Python 3.11 |
| Framework | FastAPI 0.115.0 |
| ASGI | Uvicorn 0.30.1 |
| ORM | SQLAlchemy 2.0.31 |
| DB | PostgreSQL 15 |
| Cache/Broker | Redis 7 |
| Task Queue | Celery 5.4.0 |
| Auth | JWT (python-jose) |
| HTTP | requests, httpx, aiohttp |

### Frontend

| Компонент | Версія |
|-----------|--------|
| Framework | Next.js 14.2.35 |
| React | 18.2.0 |
| TypeScript | 5.9.3 |
| Стилі | CSS (globals.css, dark theme) |

### Інфраструктура

| Сервіс | Призначення |
|--------|-------------|
| PostgreSQL | База даних (cases, timeline) |
| Redis | Кеш, Celery broker, result backend |
| Tor | SOCKS5 proxy для анонімних запитів |
| Nginx | Reverse proxy (prod profile) |
| Chromium | Web scraping у воркерах |

---

## 5. API Endpoints

### Health & Root

| Метод | Endpoint | Опис |
|-------|----------|------|
| GET | `/health` | Health check |
| GET | `/` | API info, docs link |

### Cases (Investigations)

| Метод | Endpoint | Опис |
|-------|----------|------|
| POST | `/cases` | Створити кейс |
| GET | `/cases` | Список кейсів (фільтри: priority, status, q) |
| GET | `/cases/{id}` | Деталі кейсу + timeline |
| PATCH | `/cases/{id}` | Оновити кейс |
| GET | `/cases/{id}/timeline` | Timeline |
| POST | `/cases/{id}/timeline` | Додати нотатку |

### OSINT

| Метод | Endpoint | Опис |
|-------|----------|------|
| GET | `/osint/search` | Уніфікований пошук (domain, IP, email, url) |
| GET | `/osint/verify/email` | Перевірка email (Hunter) |
| GET | `/osint/verify/domain` | Перевірка домену (placeholder) |

### Tools

| Метод | Endpoint | Опис |
|-------|----------|------|
| POST | `/tools/run` | Запуск інструменту |
| GET | `/tools/status/{task_id}` | Статус задачі |
| GET | `/tools/catalog` | Каталог інструментів |

### Auth

| Метод | Endpoint | Опис |
|-------|----------|------|
| POST | `/auth/login` | JWT login |
| POST | `/auth/refresh` | Refresh token |

---

## 6. OSINT Джерела (підключені до пошуку)

### SIGINT (Infrastructure)

- **censys-hosts** — Censys
- **fofa** — FOFA
- **zoomeye-host** — ZoomEye
- **securitytrails-dns** — SecurityTrails
- **binaryedge** — BinaryEdge
- **criminalip** — Criminal IP
- **greynoise** — GreyNoise

### HUMINT

- **hunter-email** — Hunter.io
- **sociallinks** — Social Links

### Leaks

- **hibp** — Have I Been Pwned
- **breach-directory** — Breach Directory
- **hudson-rock** — Hudson Rock
- **spycloud** — SpyCloud
- **intelligence-x** — Intelligence X
- **leak-lookup** — Leak Lookup

### Web / Open

- **urlscan** — URLScan
- **wayback-machine** — Wayback Machine
- **whois-rdap** — WHOIS/RDAP
- **alienvault-otx** — AlienVault OTX
- **virustotal** — VirusTotal
- **shodan** — Shodan
- **netlas** — Netlas
- **abuseipdb** — AbuseIPDB

**Всього:** ~23 джерела підключено до `/osint/search`.  
**Каталог:** 70+ інструментів у `tools_catalog.ts` (12 категорій).

---

## 7. Категорії інструментів

| ID | Назва | Іконка |
|----|-------|--------|
| general | OSINT | 🔍 |
| geoint | GEOINT | 🌍 |
| geosint | GEOSINT | 🛰️ |
| techint | TECHINT | ⚙️ |
| humint | HUMINT | 👤 |
| monitoring | SIGINT / WARZONE | 📡 |
| extra | ARCHINT | 📁 |
| visualization | VISINT | 📊 |
| frameworks | FRAMEWORKS | 🧩 |
| media_verification | MEDIA VERIFY | 🎥 |
| satellite | SATELLITE / MAPS | 🛰️ |
| image_infra | IMAGE / DNS / INFRA | 🖼️ |

---

## 8. Змінні середовища

### Обов'язкові

```bash
JWT_SECRET_KEY=<32+ symbols>
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://:password@host:6379/0
CELERY_BROKER_URL=redis://...
CELERY_RESULT_BACKEND=redis://...
```

### API Keys (опційно)

| Категорія | Змінні |
|-----------|--------|
| Core | OPENAI_API_KEY, SHODAN_API_KEY, HIBP_API_KEY, GEOSPY_API_KEY, PICARTA_API_KEY, YOUCONTROL_API_KEY |
| SIGINT | CENSYS_API_ID, CENSYS_API_SECRET, FOFA_TOKEN, ZOOMEYE_API_KEY, SECURITYTRAILS_KEY, BINARYEDGE_KEY, CRIMINAL_IP_KEY, GREYNOISE_KEY, NETLAS_API_KEY |
| HUMINT | HUNTER_API_KEY, SOCIAL_LINKS_KEY |
| Leaks | HUDSON_ROCK_KEY, SPYCLOUD_KEY, INTEL_X_KEY, LEAK_LOOKUP_KEY, BREACH_DIRECTORY_API_KEY |
| Threat Intel | VIRUSTOTAL_API_KEY, ALIENVAULT_KEY, ABUSEIPDB_KEY |

Повний список — `.env.example`.

---

## 9. Docker

### Сервіси

| Сервіс | Порт | Образ / Dockerfile |
|--------|------|--------------------|
| postgres | 5432 | postgres:15-alpine |
| redis | 6379 | redis:7-alpine |
| tor | 9050, 9051 | osminogin/tor-simple |
| api | 8000 | Dockerfile.api |
| worker | — | worker/Dockerfile |
| web | 3000 | web/Dockerfile |
| nginx | 80, 443 | nginx:alpine (profile prod) |

### Команди

```bash
docker-compose up -d
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d  # dev
docker-compose --profile prod up -d  # з Nginx
make up / make down / make logs / make health-check
```

---

## 10. CI/CD

**Файл:** `.github/workflows/ci-cd.yml`

**Тригери:** push/PR на `main`, `develop`

**Jobs:**

1. **test** — Python 3.11, PostgreSQL + Redis, pytest, ruff, mypy, coverage
2. **build** — Docker build (API, Worker, Web), push to ghcr.io
3. **security** — pip-audit, Bandit SAST
4. **deploy-railway** — `railway up` для API (ist) та Web (humble-presence)

**Secrets:** `RAILWAY_TOKEN`, `RAILWAY_PROJECT_ID`

---

## 11. Railway Deployment

**Конфіг:** `railway.toml`

- **API:** Dockerfile.api, healthcheck `/health`
- **Web:** окремий сервіс (Next.js)

**Змінні для API:**

- DATABASE_URL, REDIS_URL, CELERY_*, JWT_SECRET_KEY
- API keys для OSINT

**Змінні для Web:**

- NEXT_PUBLIC_API_URL (URL API на Railway)

**Addons:** PostgreSQL, Redis (через Railway Dashboard)

---

## 12. Веб-сторінки

| Шлях | Опис |
|------|------|
| `/` | Головна: пошук, метрики, категорії, підключені інструменти |
| `/control` | Сітка інструментів (Run, ToolModal) |
| `/catalog` | Каталог з фільтрами по категоріях |
| `/tools` | API Keys, управління підключеннями |
| `/investigations` | Список кейсів |

**Навігація:** Пошук, Інструменти, Каталог, API Docs

---

## 13. Документація

| Файл | Призначення |
|------|-------------|
| README.md | Головний опис, quick start |
| DEPLOYMENT.md | Повний гайд деплою |
| DOCKER_README.md | Docker quick start |
| RAILWAY_PRODUCTION.md | Railway setup |
| INDEX.md | Індекс файлів |
| USER_GUIDE.md | Користувацький гайд |
| TOOLS_47_INTEGRATION.md | Інтеграція 47 інструментів |

---

## 14. Тестування

```bash
pytest tests/ -v --cov=app
```

**Файли:** `tests/conftest.py`, `tests/test_routers.py`

---

## 15. Швидкий старт

```bash
bash docker-setup.sh
nano .env   # API keys
docker-compose up -d
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

---

*Документ згенеровано для проекту OSINT Platform 2026.*
