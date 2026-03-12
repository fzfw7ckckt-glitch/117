#!/bin/bash
# OSINT Platform 2026 - Quick Reference Card

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                   OSINT Platform 2026 - Docker Quick Reference              ║
║                           Production Ready v1.0                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─ INSTALLATION ──────────────────────────────────────────────────────────────┐
│                                                                              │
│  $ git clone <repo> osint-platform-2026                                     │
│  $ cd osint-platform-2026                                                   │
│  $ bash docker-setup.sh                                                     │
│  $ nano .env                    # Fill in API keys                          │
│  $ docker-compose up -d                                                     │
│                                                                              │
│  ✓ Frontend: http://localhost:3000                                          │
│  ✓ API Docs: http://localhost:8000/docs                                     │
│  ✓ Swagger: http://localhost:8000/redoc                                     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ QUICK COMMANDS ────────────────────────────────────────────────────────────┐
│                                                                              │
│  Using Makefile:                                                            │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │  make setup              # Full initialization               │           │
│  │  make up                 # Start services                    │           │
│  │  make down               # Stop services                     │           │
│  │  make logs               # View all logs                     │           │
│  │  make logs-api           # API logs only                     │           │
│  │  make ps                 # Show running containers           │           │
│  │  make shell-api          # Bash into API container           │           │
│  │  make health-check       # Service health status             │           │
│  │  make clean              # Remove all containers & volumes   │           │
│  └──────────────────────────────────────────────────────────────┘           │
│                                                                              │
│  Using docker-compose:                                                      │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │  docker-compose up -d              # Start all               │           │
│  │  docker-compose down               # Stop all                │           │
│  │  docker-compose ps                 # List services           │           │
│  │  docker-compose logs -f            # Follow logs             │           │
│  │  docker-compose exec api bash      # SSH to API              │           │
│  │  docker-compose restart worker     # Restart worker          │           │
│  │  docker-compose up -d --scale worker=3  # Scale workers      │           │
│  └──────────────────────────────────────────────────────────────┘           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ SERVICES & PORTS ──────────────────────────────────────────────────────────┐
│                                                                              │
│  Service           Container    Port   Status Check                         │
│  ─────────────────────────────────────────────────────────────────────────  │
│  FastAPI          osint-api     8000   curl http://localhost:8000/health    │
│  Next.js           osint-web     3000   curl http://localhost:3000          │
│  PostgreSQL        osint-postgres 5432  pg_isready -h localhost -U osint    │
│  Redis             osint-redis   6379   redis-cli ping                      │
│  Tor              osint-tor     9050   nc -zv localhost 9050               │
│  Celery Worker    osint-worker  (none)  docker logs osint-worker            │
│  Nginx (prod)     osint-nginx   80/443 curl http://localhost               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ CONFIGURATION ─────────────────────────────────────────────────────────────┐
│                                                                              │
│  Edit .env file with your values:                                           │
│                                                                              │
│  Critical:                                                                  │
│  ├─ JWT_SECRET_KEY           (auto-generated, 32+ chars)                   │
│  ├─ DB_PASSWORD              (strong password)                             │
│  ├─ REDIS_PASSWORD           (strong password)                            │
│  │                                                                          │
│  API Keys (optional, enable specific features):                            │
│  ├─ SHODAN_API_KEY           (https://www.shodan.io)                      │
│  ├─ OPENAI_API_KEY           (https://platform.openai.com)                │
│  ├─ GEOSPY_API_KEY           (https://geospy.ai)                          │
│  ├─ PICARTA_API_KEY          (https://picarta.ai)                         │
│  └─ YOUCONTROL_API_KEY       (https://youcontrol.com.ua)                  │
│                                                                              │
│  Service Ports (change if conflicts):                                      │
│  ├─ API_PORT=8000                                                          │
│  ├─ WEB_PORT=3000                                                          │
│  ├─ DB_PORT=5432                                                           │
│  └─ REDIS_PORT=6379                                                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ TROUBLESHOOTING ───────────────────────────────────────────────────────────┐
│                                                                              │
│  Problem: Port already in use                                              │
│  Solution: $ lsof -i :8000 && kill -9 <PID>                               │
│                                                                              │
│  Problem: Services won't start                                             │
│  Solution: $ docker-compose logs postgres                                 │
│            $ docker-compose down -v && docker-compose build --no-cache    │
│            $ docker-compose up -d                                         │
│                                                                              │
│  Problem: Database connection error                                        │
│  Solution: $ docker-compose exec postgres pg_isready -U osint             │
│            $ docker-compose down -v postgres                              │
│            $ docker-compose up -d postgres                                │
│            $ docker-compose exec api python scripts/init_db.py            │
│                                                                              │
│  Problem: Worker not processing tasks                                     │
│  Solution: $ docker-compose exec worker celery -A app.tasks.celery_app    │
│              inspect ping                                                 │
│            $ docker-compose restart worker                                │
│                                                                              │
│  Problem: Memory issues                                                   │
│  Solution: $ docker stats                                                 │
│            $ docker-compose exec redis redis-cli FLUSHDB                  │
│            Update docker-compose.yml resource limits                      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ DATABASE OPERATIONS ───────────────────────────────────────────────────────┐
│                                                                              │
│  Backup database:                                                           │
│  $ docker-compose exec -T postgres pg_dump -U osint osint | \             │
│    gzip > backup.sql.gz                                                    │
│                                                                              │
│  Restore database:                                                         │
│  $ gunzip < backup.sql.gz | docker-compose exec -T postgres \             │
│    psql -U osint osint                                                     │
│                                                                              │
│  Connect to database:                                                      │
│  $ docker-compose exec postgres psql -U osint -d osint                    │
│                                                                              │
│  Run migrations:                                                           │
│  $ docker-compose exec api alembic upgrade head                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ MONITORING & SCALING ──────────────────────────────────────────────────────┐
│                                                                              │
│  Resource usage:                                                            │
│  $ docker stats                                                             │
│  $ make stats                                                               │
│                                                                              │
│  Task queue:                                                                │
│  $ docker-compose exec worker celery -A app.tasks.celery_app \            │
│    inspect active                                                          │
│                                                                              │
│  Scale workers to 3:                                                       │
│  $ docker-compose up -d --scale worker=3                                  │
│                                                                              │
│  Worker concurrency (edit docker-compose.yml):                             │
│  worker:                                                                    │
│    command: celery -A app.tasks.celery_app worker \                       │
│      --concurrency=8  # Increase from 4                                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ DEVELOPMENT MODE ──────────────────────────────────────────────────────────┐
│                                                                              │
│  Start with hot reload & dev tools:                                        │
│  $ docker-compose -f docker-compose.yml \                                 │
│      -f docker-compose.dev.yml up -d                                      │
│                                                                              │
│  Additional services:                                                      │
│  ├─ pgAdmin        http://localhost:5050  (DB admin)                      │
│  ├─ Redis Commander http://localhost:8081  (Cache admin)                  │
│  └─ Adminer         http://localhost:8080  (DB inspector)                  │
│                                                                              │
│  Run tests:                                                                 │
│  $ docker-compose run --rm api pytest tests/ -v --cov=app                 │
│                                                                              │
│  Code linting:                                                             │
│  $ docker-compose run --rm api ruff check .                               │
│  $ docker-compose run --rm api mypy app/                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ PRODUCTION DEPLOYMENT ─────────────────────────────────────────────────────┐
│                                                                              │
│  1. Generate SSL certificates:                                             │
│     $ mkdir -p ssl                                                          │
│     $ openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem \            │
│       -out ssl/cert.pem -days 365 -nodes                                  │
│                                                                              │
│  2. Start with Nginx reverse proxy:                                        │
│     $ docker-compose --profile prod up -d                                 │
│                                                                              │
│  3. Access via HTTPS:                                                      │
│     https://localhost/api/docs (API)                                      │
│     https://localhost (Frontend)                                          │
│                                                                              │
│  4. Enable automatic backups:                                              │
│     Add to crontab:                                                        │
│     0 2 * * * /path/to/scripts/backup.sh                                 │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ DOCUMENTATION ─────────────────────────────────────────────────────────────┐
│                                                                              │
│  README.md              Main documentation (overview)                       │
│  DOCKER_README.md       Docker-specific guide (quick start)                │
│  DEPLOYMENT.md          Comprehensive deployment guide (12KB+)            │
│  DOCKER_SUMMARY.md      File structure & descriptions                     │
│                                                                              │
│  API Documentation:     http://localhost:8000/docs (Swagger)              │
│  API Schema:            http://localhost:8000/openapi.json                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════════╗
║                        Happy OSINT Investigating! 🔍                         ║
║                   For more help: See DEPLOYMENT.md                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

EOF
