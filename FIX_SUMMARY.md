# Підсумок виправлень

## ✅ Виконано

### 1. Web змінні додані ✅

```bash
NEXT_PUBLIC_API_URL=https://ist-production.up.railway.app
NODE_ENV=production
```

**Перевірка:**
```bash
railway variables --service humble-presence | grep -E "NEXT_PUBLIC_API_URL|NODE_ENV"
```

---

## ⚠️ Потрібно зробити вручну

### 1. Виправити Root Directory для Web

**Root Directory можна змінити ТІЛЬКИ через Dashboard UI.**

**Інструкція:**
1. Відкрий: https://railway.app/project/19bf0bd2-9e7e-45d5-adfa-9c194d9ea190/service/68c15c8a-2ae5-4bf4-a3a9-fc6ef4bd6d5f/settings
2. Розділ **Source** → **Root Directory**
3. Видали: `https://github.com/fzfw7ckckt-glitch/int`
4. Введи: `web`
5. **Save** → **Redeploy**

Детальніше: див. `FIX_ROOT_DIRECTORY.md`

---

### 2. Перевірити DATABASE_URL/REDIS_URL в addons

**Якщо addons ще не створені:**

1. **Dashboard** → **New** → **Database** → **PostgreSQL**
2. Після створення скопіюй `DATABASE_URL` з Variables addon'а
3. **ist** → **Variables** → додай `DATABASE_URL`

4. **Dashboard** → **New** → **Database** → **Redis**
5. Після створення скопіюй `REDIS_URL` з Variables addon'а
6. **ist** → **Variables** → додай:
   - `REDIS_URL`
   - `CELERY_BROKER_URL` (те саме що REDIS_URL)
   - `CELERY_RESULT_BACKEND` (те саме що REDIS_URL)

**Якщо addons вже створені:**

Змінні з addons автоматично доступні сервісам через Railway. Перевір через Dashboard:
- **ist** → **Variables** → шукай `DATABASE_URL`, `REDIS_URL`

---

## 📋 Чек-лист

- [x] `NEXT_PUBLIC_API_URL` додано для Web
- [x] `NODE_ENV` додано для Web
- [ ] Root Directory виправлено на `web` (через Dashboard)
- [ ] DATABASE_URL перевірено/додано для API
- [ ] REDIS_URL перевірено/додано для API
- [ ] Web redeploy виконано після виправлення Root Directory

---

## 🚀 Після виправлення Root Directory

```bash
# Перевірка деплою
railway deployment list --service humble-presence | head -3

# Перевірка логів
railway logs --service humble-presence --tail 30

# Перевірка доступності
curl -I https://humble-presence-production.up.railway.app

# Тест інтеграції
open https://humble-presence-production.up.railway.app
```

---

**Останнє оновлення:** 12 березня 2026
