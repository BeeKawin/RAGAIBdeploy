# Deployment File Manifest

Use this when you want to commit or review only the Vercel/Railway hosting work.

The repo can contain many unrelated data, scraping, evaluation, and index changes. Do not use `git add .` when preparing a deployment commit unless you intentionally want all of those changes.

## Show Deployment Files

From `ragaib/`:

```powershell
.\scripts\list_deployment_files.ps1
```

If Windows blocks local scripts, use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\list_deployment_files.ps1
```

This prints the files that are part of the current hosting setup and a selective `git add` command.

## Review Deployment Diff

From `ragaib/`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\show_deployment_diff.ps1
```

This is read-only. It shows git status and diff only for deployment-related files, so unrelated scraper data or evaluation artifacts do not bury the changes you actually need to review.

## Deployment-Related Files

```text
.dockerignore
.env.example
.github/workflows/predeploy.yml
.gitattributes
Dockerfile
README.md
railway.json
chat/api.py
config/settings.py
demo/app.js
demo/config.js
demo/index.html
demo/styles.css
demo/vercel.json
docs/DEMO_AND_DEPLOYMENT.md
docs/DEPLOYMENT_HANDOFF.md
docs/DEPLOYMENT_FILE_MANIFEST.md
docs/DEPLOYMENT_STATUS_CHECKLIST.md
docs/DEPLOYMENT_TROUBLESHOOTING.md
docs/GIT_DEPLOYMENT_WORKFLOW.md
docs/RAILWAY_ENV_VARS.md
docs/VERCEL_SETUP.md
docs/VERCEL_RAILWAY_DEPLOYMENT.md
scripts/check_deployment.ps1
scripts/list_deployment_files.ps1
scripts/predeploy_check.ps1
scripts/railway_index.sh
scripts/show_deployment_diff.ps1
tests/test_demo_site.py
tests/test_source_routing.py
vector_store/indexer.py
```

## Safe Editing Rule

- Frontend-only edits usually live in `demo/`.
- Backend deployment edits usually live in `Dockerfile`, `railway.json`, `.dockerignore`, `.env.example`, `chat/api.py`, or `config/settings.py`.
- Runtime secrets belong in Railway/Vercel dashboards or local `.env`, never in committed files.
- The generated vector DB belongs on Railway persistent storage, not in Git.
