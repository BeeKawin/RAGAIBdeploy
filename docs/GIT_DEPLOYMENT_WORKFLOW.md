# Git Deployment Workflow

Use this guide to keep local experimentation separate from the deployed demo.

## First GitHub Push

For the first deployment, GitHub needs the whole application, not only the Vercel/Railway files. Commit the project code, tests, normalized data needed for indexing, and scraper/indexing pipeline files.

Railway indexing depends on:

```text
data/normalized/
```

That folder should be committed for the first deployment.

Do not commit:

```text
.env
.venv/
vector_db/
data/eval/results/
data/eval/summaries/
data/eval/live_queries/
__pycache__/
.pytest_cache/
```

Run this before committing:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\predeploy_check.ps1
```

After pushing, GitHub Actions runs `.github/workflows/predeploy.yml` on `main` and pull requests. It verifies tests, deployment JSON, and normalized indexing inputs.

Then inspect what Git will include:

```powershell
git status --short
```

For the first push, it is normal to include core folders such as:

```text
chat/
config/
demo/
docs/
embeddings/
evaluation/
retrieval/
scraper/
scripts/
tests/
vector_store/
data/normalized/
```

## Deployment-Only Updates

After the first working deployment, use the deployment manifest when you only changed hosting, demo UI, CORS, Railway, or Vercel settings:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\show_deployment_diff.ps1
powershell -ExecutionPolicy Bypass -File scripts\list_deployment_files.ps1
```

Use the printed selective `git add ...` command only when you intentionally want a deployment-only commit.

## Safe Branch Flow

Recommended:

```powershell
git switch main
git pull
git switch -c feature/my-change
```

Work locally on the feature branch. Push the branch to GitHub and let Vercel create a preview deployment. Keep Railway production connected to `main`.

Only merge into `main` when:

- local tests pass
- Railway/Vercel preview looks correct
- secrets are not in Git
- generated vector DB files are not in Git

## Environment Safety

Local `.env` is for your machine only. Railway and Vercel environment variables are configured in their dashboards.

Use:

```text
.env.example
```

as documentation, not as a real secret store.

## Vector DB Safety

Do not commit `vector_db/`. For production:

1. Railway mounts persistent storage at `/app/vector_db`.
2. You run `python -m vector_store.indexer` on Railway.
3. Railway keeps the Chroma DB and Hugging Face cache on that persistent disk.

Local changes to your vector DB will not affect production unless you rerun indexing on Railway.
