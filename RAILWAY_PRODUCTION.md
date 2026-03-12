# Railway Production Setup

## Addons (PostgreSQL, Redis)

Для повноцінної роботи API з БД та Celery:

### 1. PostgreSQL

1. Railway Dashboard → проект → **New** → **Database** → **PostgreSQL**
2. Після створення: **Variables** → скопіюй `DATABASE_URL`
3. API service → **Variables** → додай `DATABASE_URL` = значення з addon

### 2. Redis

1. Railway Dashboard → проект → **New** → **Database** → **Redis**
2. Після створення: **Variables** → скопіюй `REDIS_URL`
3. API service → **Variables** → додай:
   - `REDIS_URL` = значення з addon
   - `CELERY_BROKER_URL` = те саме (або `REDIS_URL`)
   - `CELERY_RESULT_BACKEND` = те саме

### 3. GitHub Actions Auto-Deploy

1. Railway Dashboard → **Settings** → **Tokens** → створи **Project Token**
2. GitHub → репо → **Settings** → **Secrets and variables** → **Actions**
3. Додай secret `RAILWAY_TOKEN` = значення токена
4. При push у `main` / `develop` — автоматичний deploy API та Web

### 4. Змінні для API

Мінімальний набір:

```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
CELERY_BROKER_URL=redis://...
CELERY_RESULT_BACKEND=redis://...
JWT_SECRET_KEY=<random 32+ chars>
```

Опційно — API ключі для OSINT інструментів (Shodan, Censys, HIBP тощо).

### 5. Змінні для Web

```
NEXT_PUBLIC_API_URL=https://ist-production.up.railway.app
```

(або URL твого API сервісу)
