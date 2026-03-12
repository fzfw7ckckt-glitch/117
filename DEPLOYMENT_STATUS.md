# Deployment Status — OSINT Platform 2026

**Оновлено:** 12.03.2026

## Що зроблено

### 1. Виправлення Docker build

- **docker-compose.yml**: прибрано deprecated `version: '3.8'`
- **Redis healthcheck**: додано пароль (`-a ${REDIS_PASSWORD}`) для коректної перевірки
- **web/Dockerfile**: коректна робота з `public/` (mkdir + COPY)
- **web/.dockerignore**: додано для швидшого білду (node_modules, .next)
- **.dockerignore**: виключено `web/node_modules`, `web/.next` з контексту API/worker

### 2. Оптимізація requirements (менший розмір образів)

- **requirements-api.txt**: легкий набір для API (без ML: TensorFlow, PyTorch, deepface)
- **requirements-worker.txt**: базовий набір + selenium, openai, pillow
- **Dockerfile.api**: використовує `requirements-api.txt`
- **worker/Dockerfile**: використовує `requirements-worker.txt`

Це зменшило розмір образів і час білду.

### 3. Додаткові файли

- `web/public/favicon.svg` — placeholder для public
- `requirements-api.txt`, `requirements-worker.txt` — розділені залежності

## Як запустити

```bash
# 1. Скопіюй .env
cp .env.example .env
# Відредагуй JWT_SECRET_KEY, паролі БД/Redis

# 2. Запуск
docker-compose up -d --build

# 3. Перевірка
docker-compose ps
curl http://localhost:8000/health
curl http://localhost:3000
```

## Порти

- **API**: 8000
- **Web**: 3000
- **PostgreSQL**: 5432
- **Redis**: 6379
- **Tor SOCKS5**: 9050

## Попередження при запуску

Якщо бачиш `ABUSEIPDB_KEY` / `HYBRID_ANALYSIS_KEY` not set — це нормально. Додай їх у `.env`, якщо використовуєш ці інструменти.

## Backend тести

```bash
cd /Users/admin/Desktop/osint-platform-2026
python -m pytest tests/ -v
```

## Deploy на Railway

Див. `DEPLOYMENT.md`, `railway.toml`, `web/railway.toml`.
