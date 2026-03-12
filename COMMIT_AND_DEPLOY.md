# Коміт і редеплой — завершено

## Виконані зміни

### 1. Виправлення page.tsx
- **Видалено** дублікат `export default` (Dashboard перезаписував HomePage і викликав ReferenceError)
- **Збережено** параметри URL при редіректі: `/?tool=shodan` → `/control?tool=shodan`

### 2. Кнопка Run
- **ToolCard, ToolModal, ToolInspector**: Run відкриває `/control?tool=X` замість `/?q=&tool=X`
- **Control page**: читає `?tool=` з URL і відкриває модальне вікно інструменту
- **Suspense**: обгортка для `useSearchParams` (Next.js 14)

### 3. Видалення інструментації
- Видалено всі `_dbg` та інші debug-логії з AppContext, ToolSearchBar, ToolCard, ToolModal

### 4. Тести
- **Backend**: 19 passed
- **API**: health, osint/search, cases — працюють
- **Web**: control, catalog, investigations — доступні

## Коміт

```
aca9362 fix: Run button tool param, remove duplicate Dashboard, preserve URL params
```

**14 файлів змінено**

## Редеплой

### Варіант 1: Push у main (автоматичний deploy)

```bash
git checkout main
git merge refactor/osint-ui-quick
git push origin main
```

CI/CD запустить deploy на Railway при push у `main` або `develop`.

### Варіант 2: Merge через PR

1. Створити PR: `refactor/osint-ui-quick` → `main`
2. Перевірити CI (test, build)
3. Змерджити в main
4. Deploy автоматично запуститься

### Варіант 3: Railway CLI (ручний deploy)

```bash
cd web
railway link -p 19bf0bd2-9e7e-45d5-adfa-9c194d9ea190 -e production
railway up --service humble-presence
```

## Перевірка після деплою

1. `/control` — відкривається
2. Клік по картці інструменту → модальне вікно
3. Кнопка Run → `/control?tool=shodan` → модальне вікно
4. `/investigations` — CRUD cases
5. `/catalog` — каталог інструментів
