# Railway + int repo

## Репо

**[fzfw7ckckt-glitch/int](https://github.com/fzfw7ckckt-glitch/int)** — osint base pipeline

Структура:
```
int/
├── int-main/          ← Root Directory для Railway
│   ├── backend/
│   ├── frontend/
│   ├── docker-compose.yml
│   └── ...
├── LICENSE
└── README.md
```

## Railway: Root Directory

Якщо помилка `Could not find root directory: https://github.com/fzfw7ckckt-glitch/int`:

1. **Settings** → **Source** → **Root Directory**
2. Видалити URL, ввести: **`int-main`**
3. **Save** → **Redeploy**

## Локальний запуск (int-main)

```bash
# Клонувати
git clone https://github.com/fzfw7ckckt-glitch/int
cd int/int-main

# Docker
docker-compose up -d

# Frontend: http://localhost:3000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```
