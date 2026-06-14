# Deployment Status Checklist

Use this as the live checklist while deploying the demo.

## Prepared In The Repo

- [x] Static demo UI exists in `demo/`.
- [x] Demo UI can call either same-origin local FastAPI or a remote API base URL.
- [x] Vercel static config exists at `demo/vercel.json`.
- [x] Railway Docker config exists at `Dockerfile`.
- [x] Railway service config exists at `railway.json`.
- [x] Backend CORS is configurable with `ALLOWED_ORIGINS`.
- [x] Railway `/health` can report vector status without loading BGE-M3.
- [x] Safe env template exists at `.env.example`.
- [x] Deployment check script exists at `scripts/check_deployment.ps1`.
- [x] Deployment file manifest exists at `scripts/list_deployment_files.ps1`.
- [x] Deployment-only diff helper exists at `scripts/show_deployment_diff.ps1`.
- [x] Local predeploy check exists at `scripts/predeploy_check.ps1`.
- [x] Railway indexing helper exists at `scripts/railway_index.sh`.
- [x] Git workflow guide explains first push vs deployment-only updates.
- [x] Railway env-var copy sheet exists at `docs/RAILWAY_ENV_VARS.md`.
- [x] Vercel setup sheet exists at `docs/VERCEL_SETUP.md`.
- [x] Deployment troubleshooting guide exists at `docs/DEPLOYMENT_TROUBLESHOOTING.md`.
- [x] GitHub Actions predeploy workflow exists at `.github/workflows/predeploy.yml`.

## Your Railway Actions

- [ ] Rotate the OpenRouter API key before deploying.
- [ ] Push the full application to GitHub for the first deployment.
- [ ] Confirm GitHub Actions predeploy workflow passes on `main`.
- [ ] Create a Railway project from the GitHub repo.
- [ ] Set Railway root directory to `ragaib`.
- [ ] Add environment variables from `docs/RAILWAY_ENV_VARS.md`.
- [ ] Set `ALLOWED_ORIGINS` to your Vercel production URL.
- [ ] Add persistent storage mounted at `/app/vector_db`.
- [ ] Deploy the backend.
- [ ] Run `python -m vector_store.indexer` or `sh scripts/railway_index.sh` in Railway.
- [ ] Confirm `/health` reports `total_chunks > 0`.

## Your Vercel Actions

- [ ] Open `docs/VERCEL_SETUP.md`.
- [ ] Create a Vercel project from the same GitHub repo.
- [ ] Set Vercel root directory to `ragaib/demo`.
- [ ] Leave build command blank.
- [ ] Deploy the frontend.
- [ ] Enter the Railway API URL in the demo page's **API Base URL** field.
- [ ] After the URL is stable, optionally set it in `demo/config.js`.

## Final Verification

From `ragaib/`, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_deployment.ps1 `
  -ApiBaseUrl "https://your-railway-api-url" `
  -FrontendOrigin "https://your-vercel-site.vercel.app"
```

The deployment is ready to present when this passes and the Vercel page shows:

- RAG answer
- baseline answer
- retrieved chunks
- RAG scores
- baseline scores
- winner and comparison rationale

## Safe Editing Rule

Keep production deployments connected to `main`. Do experimental changes on branches and use preview deployments. Do not commit `.env`, `.venv/`, `vector_db/`, or generated evaluation outputs.

Before committing deployment changes, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\predeploy_check.ps1
powershell -ExecutionPolicy Bypass -File scripts\show_deployment_diff.ps1
powershell -ExecutionPolicy Bypass -File scripts\list_deployment_files.ps1
```
