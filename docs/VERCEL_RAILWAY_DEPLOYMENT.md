# Vercel + Railway Deployment Guide

This project should deploy as two separate services:

- **Vercel**: static demo website from `demo/`
- **Railway**: Python FastAPI backend from the project root

This keeps the frontend easy to edit while the heavy RAG backend keeps its own environment, vector DB, and secrets.

## Why Split Deployment

The backend loads:

- Chroma vector DB
- BGE-M3 embeddings
- sentence-transformers
- OpenRouter API calls

This is too heavy for a simple Vercel static deployment. Vercel should serve the UI only.

## Files Added For Deployment

```text
demo/vercel.json       Vercel static hosting config
demo/config.js         Runtime frontend API base URL
Dockerfile             Railway backend container
railway.json           Railway deploy config
.dockerignore          Keeps local/generated files out of Railway builds
.env.example           Safe env var template
.github/workflows/predeploy.yml  GitHub test gate before deployment
.gitattributes         Keeps Linux deployment scripts using LF endings
docs/DEPLOYMENT_HANDOFF.md  Short end-to-end deployment sequence
scripts/check_deployment.ps1  Verifies deployed Railway/Vercel wiring
scripts/list_deployment_files.ps1  Lists files to stage for deployment commits
scripts/predeploy_check.ps1  Runs local checks before pushing deployment changes
scripts/railway_index.sh  Railway/Linux helper for one-off vector indexing
scripts/show_deployment_diff.ps1  Reviews only deployment-related changes
docs/DEPLOYMENT_STATUS_CHECKLIST.md  Tracks prepared work vs. your dashboard actions
docs/RAILWAY_ENV_VARS.md  Copy sheet for Railway environment variables
docs/VERCEL_SETUP.md  Copy sheet for Vercel frontend settings
docs/DEPLOYMENT_TROUBLESHOOTING.md  Common Railway/Vercel failure fixes
```

## Step 1: Prepare GitHub

You do this part.

1. Commit and push the repo to GitHub.
2. Make sure `.env`, `.venv/`, `vector_db/`, and generated eval files are not committed.
3. Keep local development on your normal branch.
4. Use Vercel/Railway preview deployments for branches so experimenting locally does not break production.
5. Keep production deployment connected to `main`; use other branches for risky changes.

For the first GitHub push, read:

```text
docs/GIT_DEPLOYMENT_WORKFLOW.md
```

The deployment manifest is for deployment-only updates. The first deployment still needs the full application code and normalized data needed for indexing.

Before committing only the deployment work, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\predeploy_check.ps1
```

Then inspect the deployment file list:

```powershell
.\scripts\list_deployment_files.ps1
```

If Windows blocks script execution, use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\list_deployment_files.ps1
```

This helps you avoid accidentally committing local raw data, generated eval results, or vector DB artifacts.

To review only deployment-related changes before committing:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\show_deployment_diff.ps1
```

## Step 2: Deploy Backend On Railway

You do this part in Railway.

1. Create a new Railway project.
2. Choose **Deploy from GitHub repo**.
3. Set the service root directory to:
   ```text
   ragaib
   ```
4. Railway should detect `railway.json` and `Dockerfile`.
5. Add environment variables from `docs/RAILWAY_ENV_VARS.md`:
   ```env
   LLM_PROVIDER=openrouter
   LLM_MODEL=openrouter/free
   JUDGE_PROVIDER=openrouter
   JUDGE_MODEL=openrouter/free
   BASELINE_PROVIDER=openrouter
   BASELINE_MODEL=openrouter/free
   OPENROUTER_API_KEY=your_real_key
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   OPENROUTER_APP_NAME=RAGAI-B-Demo
   OPENROUTER_SITE_URL=https://your-vercel-site.vercel.app
   ALLOWED_ORIGINS=https://your-vercel-site.vercel.app
   EMBEDDING_MODEL=BAAI/bge-m3
   EMBEDDING_DIMENSION=1024
   CHROMA_COLLECTION=ragaib_bge_m3_v1
   HF_HOME=/app/vector_db/huggingface
   ```
6. Add persistent storage if your Railway plan supports it.
7. Mount persistent storage to:
   ```text
   /app/vector_db
   ```
8. This stores both the Chroma vector DB and the Hugging Face model cache.
9. Deploy the backend.

## Step 3: Build The Vector DB On Railway

You do this part after Railway deploys.

The `/health` endpoint is intentionally lightweight: it checks Chroma collection metadata and chunk count without forcing BGE-M3 to load. BGE-M3 loads during indexing and retrieval.

In Railway shell or one-off command, run:

```bash
python -m vector_store.indexer
```

Or, if Railway exposes a shell command runner:

```bash
sh scripts/railway_index.sh
```

Then check:

```text
https://your-railway-api-url/health
```

Expected:

```json
{
  "status": "ok",
  "vector_store": {
    "collection": "ragaib_bge_m3_v1",
    "embedding_model": "BAAI/bge-m3",
    "embedding_dim": 1024,
    "total_chunks": 1
  }
}
```

`total_chunks` should be much larger than `1` after a full index. If it is `0`, indexing did not complete.

## Step 4: Deploy Frontend On Vercel

You do this part in Vercel.

Use `docs/VERCEL_SETUP.md` as the focused setup sheet.

1. Create a new Vercel project from the same GitHub repo.
2. Set the project root directory to:
   ```text
   ragaib/demo
   ```
3. No build command is required.
4. No output directory is required.
5. Deploy.

## Step 5: Connect Vercel Frontend To Railway Backend

Option A: edit `demo/config.js` before deploying:

```js
window.RAGAIB_API_BASE_URL = "https://your-railway-api-url";
```

Option B: leave `config.js` blank and enter the API URL in the demo page's **API Base URL** input. The browser saves it in `localStorage`.

Recommended for early testing:

- Use Option B first.
- Once the Railway URL is stable, set Option A.

## Step 6: Test Production Demo

From your local machine, you can first run:

```powershell
.\scripts\check_deployment.ps1 `
  -ApiBaseUrl "https://your-railway-api-url" `
  -FrontendOrigin "https://your-vercel-site.vercel.app"
```

If Windows blocks script execution, use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_deployment.ps1 `
  -ApiBaseUrl "https://your-railway-api-url" `
  -FrontendOrigin "https://your-vercel-site.vercel.app"
```

This checks:

- Railway `/health`
- vector DB chunk count
- CORS from your Vercel domain
- `POST /eval/live-query`

In the Vercel site:

1. Enter your Railway API URL.
2. Ask:
   ```text
   What is Newton's second law?
   ```
3. Select:
   ```text
   subject = physics
   grade = M4
   language = EN
   answer type = homework-help
   ```
4. Confirm the page shows:
   - RAG answer
   - baseline answer
   - retrieved chunks
   - RAG scores
   - baseline scores
   - winner and comparison

If any of these fail, use:

```text
docs/DEPLOYMENT_TROUBLESHOOTING.md
```

## Safe Editing Workflow

To keep editing from breaking the deployed system:

1. Keep production deployments on `main`.
2. Create feature branches for experiments.
3. Vercel will create preview deployments for branches.
4. Railway can also deploy from a selected branch; keep production pointed at `main`.
5. Do not edit production environment variables for experiments.
6. Use `.env` locally and `.env.example` as documentation only.
7. Do not commit `vector_db/`; rebuild it on Railway persistent disk when needed.
8. Keep `demo/config.js` blank while testing; use the page's API Base URL field until the backend URL is stable.
9. After the backend URL is stable, update `demo/config.js` on `main` once, then use preview branches for future UI changes.
10. Keep Railway `ALLOWED_ORIGINS` pointed at production Vercel. For preview frontend deployments, temporarily add that preview URL as a comma-separated value.

## When You Need To Take Action

You must do these manually:

- Create/link GitHub repo.
- Create Railway service.
- Add Railway environment variables.
- Add Railway persistent storage.
- Run the Railway indexing command once.
- Run `scripts/check_deployment.ps1` after Railway and Vercel are live.
- Use `scripts/list_deployment_files.ps1` before making a deployment-only commit.
- Create Vercel project.
- Set Vercel root directory to `ragaib/demo`.
- Enter or configure the Railway API URL in the frontend.

Codex can prepare files and commands, but it cannot click through Railway/Vercel dashboards for you.
