# Web version without your Mac

To use the platform from any browser (phone, tablet, another PC) without your Mac:

## 1. API (already on Railway)

- In [Railway](https://railway.com) → your project → **API service** → **Settings** → **Networking**.
- Click **Generate Domain** (or use an existing one). You’ll get a URL like `https://your-api-name.up.railway.app`.
- Use that URL for:
  - **API docs:** `https://your-api-name.up.railway.app/docs`
  - **Health:** `https://your-api-name.up.railway.app/health`

## 2. Web frontend (deploy on Railway)

1. In the same Railway project, click **New** → **GitHub Repo** (or **Empty Service** if you deploy with CLI).
2. If using GitHub: connect the repo, then for the **new service**:
   - **Settings** → **Root Directory:** set to `web`.
   - **Settings** → **Build:** Dockerfile (use `web/Dockerfile`).
   - **Variables:** add `NEXT_PUBLIC_API_URL` = your API URL from step 1 (e.g. `https://your-api-name.up.railway.app`).
3. Deploy. Railway will build the Next.js app and give you a URL like `https://your-web-name.up.railway.app`.

If you deploy with CLI from the repo root (and the new service is set to root directory `web`):

```bash
railway link --project <project-id> --environment production
railway up --service <web-service-id>
```

## 3. Use from any device

- **Web UI:** open the web service URL (e.g. `https://your-web-name.up.railway.app`) in any browser.
- **API:** open the API URL (e.g. `https://your-api-name.up.railway.app/docs`) for Swagger.

No need to have your Mac running or connected.
