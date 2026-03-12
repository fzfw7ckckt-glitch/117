# osint-platform-docker.zip

Архів для Docker-деплою (int-main, 57 tools).

## Вміст

- `backend/` — FastAPI, 57 інструментів
- `frontend/` — Next.js 14, MUI
- `docker-compose.yml` — postgres, redis, api, celery, frontend

## Запуск

```bash
unzip osint-platform-docker.zip
cd osint-platform-docker  # або папка після розпакування
docker-compose up -d
```

- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs

## Примітка

Після розпакування `frontend/` не містить `node_modules` — Docker збирає їх під час build.
