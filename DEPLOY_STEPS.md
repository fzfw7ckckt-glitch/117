# Поетапний деплой OSINT Platform 2026 на Railway

> **Дата:** 12 березня 2026  
> **Проект:** sparkling-enjoyment  
> **Сервіси:** ist (API), humble-presence (Web)

---

## 📋 Передумови

- [ ] GitHub репозиторій підключено до Railway
- [ ] Railway CLI встановлено (`railway --version`)
- [ ] Доступ до Railway Dashboard
- [ ] API ключі для OSINT інструментів готові

---

## Етап 1: Підготовка проекту

### 1.1 Перевірка файлів

```bash
cd /Users/admin/Desktop/osint-platform-2026

# Перевірка Dockerfiles
ls -la Dockerfile.api web/Dockerfile worker/Dockerfile

# Перевірка конфігурацій
ls -la railway.toml web/railway.toml

# Перевірка .env.example
cat .env.example
```

**Очікуваний результат:**
- ✅ `Dockerfile.api` існує
- ✅ `web/Dockerfile` існує
- ✅ `worker/Dockerfile` існує
- ✅ `railway.toml` існує
- ✅ `web/railway.toml` існує

---

## Етап 2: Налаштування Railway проекту

### 2.1 Створення/перевірка проекту

1. Відкрий: https://railway.app/dashboard
2. Перевір проект: **sparkling-enjoyment** (ID: `19bf0bd2-9e7e-45d5-adfa-9c194d9ea190`)
3. Environment: **production**

### 2.2 Створення Addons (якщо ще немає)

#### PostgreSQL
1. **New** → **Database** → **PostgreSQL**
2. Після створення скопіюй `DATABASE_URL`
3. Формат: `postgresql://user:pass@host:port/dbname`

#### Redis
1. **New** → **Database** → **Redis**
2. Скопіюй `REDIS_URL`
3. Формат: `redis://:password@host:port/0`

**Перевірка:**
```bash
railway variables --project 19bf0bd2-9e7e-45d5-adfa-9c194d9ea190 | grep -i "DATABASE_URL\|REDIS_URL"
```

---

## Етап 3: Деплой API (ist)

### 3.1 Підключення сервісу

```bash
cd /Users/admin/Desktop/osint-platform-2026

# Підключення до проекту
railway link --project 19bf0bd2-9e7e-45d5-adfa-9c194d9ea190

# Вибір сервісу ist
railway service ist
```

### 3.2 Налаштування через Dashboard

1. **ist** → **Settings** → **Source**
   - **Root Directory:** порожнє (або `.`)
   - **Dockerfile path:** `Dockerfile.api` (або залишити автоматичне)

2. **Settings** → **Variables**
   - Додай змінні з `.env.example`:
     ```
     DATABASE_URL=<з PostgreSQL addon>
     REDIS_URL=<з Redis addon>
     CELERY_BROKER_URL=<REDIS_URL>
     CELERY_RESULT_BACKEND=<REDIS_URL>
     JWT_SECRET_KEY=<генеруй: openssl rand -hex 32>
     ```
   - Додай API keys для OSINT (Shodan, Censys, HIBP тощо)

### 3.3 Деплой

```bash
# З кореня репо
railway up --service ist
```

**Або через GitHub:**
- Зроби push у `main` → автоматичний деплой через CI/CD

### 3.4 Перевірка

```bash
# Перевірка статусу
railway status --service ist

# Перевірка логів
railway logs --service ist | tail -50

# Перевірка healthcheck
curl https://ist-production.up.railway.app/health
```

**Очікуваний результат:**
- ✅ Deployment статус: `SUCCESS`
- ✅ Healthcheck: `{"status":"ok"}`
- ✅ Логи без критичних помилок

---

## Етап 4: Деплой Web (humble-presence)

### 4.1 Виправлення Root Directory ⚠️

**КРИТИЧНО:** Виправити помилку Root Directory!

1. **humble-presence** → **Settings** → **Source**
2. **Root Directory:** 
   - ❌ Видалити: `https://github.com/fzfw7ckckt-glitch/int`
   - ✅ Встановити: `web`
3. **Зберегти**

### 4.2 Налаштування змінних

**Settings** → **Variables**:
```
NEXT_PUBLIC_API_URL=https://ist-production.up.railway.app
NODE_ENV=production
```

### 4.3 Деплой

```bash
# З папки web
cd web
railway service humble-presence
railway up
```

**Або через GitHub:**
- Push у `main` → CI/CD автоматично деплоїть

### 4.4 Перевірка

```bash
# Статус
railway status --service humble-presence

# Логи
railway logs --service humble-presence | tail -50

# Перевірка сайту
curl -I https://humble-presence-production.up.railway.app
```

**Очікуваний результат:**
- ✅ Deployment статус: `SUCCESS`
- ✅ Сайт відкривається (HTTP 200)
- ✅ UI завантажується коректно

---

## Етап 5: Перевірка інтеграції

### 5.1 Перевірка API з Web

1. Відкрий: https://humble-presence-production.up.railway.app
2. Перевір:
   - ✅ Метрики відображаються
   - ✅ OSINT пошук працює
   - ✅ Інструменти завантажуються
   - ✅ API Docs посилання працює

### 5.2 Тестування OSINT пошуку

1. Введи тестовий запит: `example.com`
2. Перевір:
   - ✅ Запит відправляється на API
   - ✅ Результати відображаються
   - ✅ Немає CORS помилок

### 5.3 Перевірка змінних

```bash
# API змінні
railway variables --service ist | grep -E "DATABASE_URL|REDIS_URL|JWT_SECRET"

# Web змінні
railway variables --service humble-presence | grep "NEXT_PUBLIC_API_URL"
```

---

## Етап 6: Оптимізація та моніторинг

### 6.1 Налаштування моніторингу

1. **Railway Dashboard** → **Metrics**
2. Перевір:
   - CPU використання
   - Memory використання
   - Network трафік

### 6.2 Налаштування алертів (опційно)

1. **Settings** → **Notifications**
2. Додай email для алертів про помилки

### 6.3 Перевірка логів

```bash
# API логи
railway logs --service ist --tail 100

# Web логи
railway logs --service humble-presence --tail 100
```

---

## Етап 7: Фінальна перевірка

### 7.1 Чек-лист

- [ ] API деплой успішний (`ist`)
- [ ] Web деплой успішний (`humble-presence`)
- [ ] Root Directory виправлено (`web`)
- [ ] Змінні налаштовані (DATABASE_URL, REDIS_URL, JWT_SECRET, NEXT_PUBLIC_API_URL)
- [ ] Healthcheck працює (`/health`)
- [ ] Сайт відкривається
- [ ] OSINT пошук працює
- [ ] Немає критичних помилок в логах

### 7.2 Тестові URL

| Сервіс | URL | Очікуваний результат |
|--------|-----|----------------------|
| API | https://ist-production.up.railway.app/health | `{"status":"ok"}` |
| API Docs | https://ist-production.up.railway.app/docs | Swagger UI |
| Web | https://humble-presence-production.up.railway.app | Dashboard |

---

## 🚨 Troubleshooting

### Проблема: Root Directory помилка

**Симптом:** `Root Directory https://github.com/... does not exist`

**Рішення:**
1. Dashboard → humble-presence → Settings → Source
2. Root Directory: `web`
3. Save → Redeploy

### Проблема: API не підключається до БД

**Симптом:** `could not connect to database`

**Рішення:**
1. Перевір `DATABASE_URL` в Variables
2. Перевір, що PostgreSQL addon запущений
3. Перевір network connectivity

### Проблема: Web не підключається до API

**Симптом:** CORS помилки або `Failed to fetch`

**Рішення:**
1. Перевір `NEXT_PUBLIC_API_URL` в Variables
2. Перевір CORS налаштування в API (`main.py`)
3. Перевір, що API доступний

---

## 📝 Нотатки

- **API Service ID:** `eee77f55-73ed-4b5b-8439-86f9b366faaf`
- **Web Service ID:** `68c15c8a-2ae5-4bf4-a3a9-fc6ef4bd6d5f`
- **Project ID:** `19bf0bd2-9e7e-45d5-adfa-9c194d9ea190`
- **Environment ID:** `f3452065-3ae7-49ed-8209-428076b4aee2`

---

## ✅ Після успішного деплою

1. Зроби backup змінних середовища
2. Документуй зміни
3. Налаштуй моніторинг
4. Протестуй всі функції

---

**Останнє оновлення:** 12 березня 2026
