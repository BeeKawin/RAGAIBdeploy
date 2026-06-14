# Deployment Handoff

This is the short version of the Vercel/Railway deployment flow.

## 1. Local Predeploy Check

From `ragaib/`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\predeploy_check.ps1
```

This must pass before pushing deployment changes.

## 2. GitHub

For the first deployment, push the full application to GitHub.

Make sure `data/normalized/` is included, because Railway builds the vector DB from those files.

Do not commit:

```text
.env
.venv/
vector_db/
data/eval/results/
data/eval/summaries/
data/eval/live_queries/
```

For deployment-only updates later, use the selective file list printed by:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\list_deployment_files.ps1
```

## 3. Railway Backend First

In Railway:

```text
Root Directory: ragaib
Builder: Dockerfile
Persistent Volume Mount: /app/vector_db
```

Copy env vars from:

```text
docs/RAILWAY_ENV_VARS.md
```

Deploy the backend.

After deploy, run:

```bash
sh scripts/railway_index.sh
```

Check:

```text
https://your-railway-api-url/health
```

`total_chunks` must be greater than `0`.

## 4. Vercel Frontend Second

In Vercel:

```text
Root Directory: ragaib/demo
Framework Preset: Other
Build Command: leave blank
Output Directory: leave blank
Install Command: leave blank
```

Use:

```text
docs/VERCEL_SETUP.md
```

After Vercel gives you a URL, update Railway:

```env
ALLOWED_ORIGINS=https://your-vercel-site.vercel.app
OPENROUTER_SITE_URL=https://your-vercel-site.vercel.app
```

Restart/redeploy Railway after changing env vars.

## 5. Final Verification

From `ragaib/`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_deployment.ps1 `
  -ApiBaseUrl "https://your-railway-api-url" `
  -FrontendOrigin "https://your-vercel-site.vercel.app"
```

Then open the Vercel page and test:

```text
Question: What is Newton's second law?
Subject: physics
Grade: M4
Language: EN
Answer type: homework-help
```

The demo is ready when it shows:

- RAG answer
- baseline answer
- retrieved chunks
- RAG scores
- baseline scores
- winner and comparison rationale

## Safe Editing Rule

Keep production on `main`. Use feature branches and preview deployments for experiments. Local `.env`, local `vector_db/`, and generated eval outputs should never be committed.
