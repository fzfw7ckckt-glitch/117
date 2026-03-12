# OSINT Platform 2026 — User Guide

## Швидкий старт

### 1. Локальний запуск (Docker)

```bash
cp .env.example .env
# Відредагуй .env — мінімум: JWT_SECRET_KEY, DB_PASSWORD, REDIS_PASSWORD
docker-compose up -d
```

- **Web:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs

### 2. OSINT-пошук

1. Відкрий головну сторінку або `/tools`
2. Введи запит: домен, IP, email, username
3. Натисни **Пошук** — результати з усіх підключених джерел з’являться в таблиці

### 3. Control Dashboard (`/control`)

- **Quick Sets:** Network Scan, Email Hunt, Social Search, Photo Check — пресети для фільтрації інструментів
- **Toggle:** вмикай/вимикай інструменти для пошуку
- **Save Config:** конфігурація зберігається в localStorage
- **Tool Info:** клік по інструменту — деталі та Run Query

### 4. API-ключі

Мінімальний набір для пошуку (додай у `.env` або Railway Variables):

| Інструмент | Змінна | Де взяти |
|------------|--------|----------|
| Shodan | `SHODAN_API_KEY` | shodan.io |
| Censys | `CENSYS_API_ID`, `CENSYS_API_SECRET` | censys.io |
| VirusTotal | `VIRUSTOTAL_API_KEY` | virustotal.com |
| HIBP | `HIBP_API_KEY` | haveibeenpwned.com |
| Hunter.io | `HUNTER_API_KEY` | hunter.io |

Повний список — `.env.example`.

### 5. Передача ключів через UI

На сторінці `/control` можна додати ключі через **Settings** (X-User-Keys) — вони передаються в заголовку запиту і мають пріоритет над `.env`.
