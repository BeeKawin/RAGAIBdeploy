# Deployment Troubleshooting

Use this when the Vercel demo or Railway backend does not behave as expected.

## Railway `/health` Fails

Check Railway logs first.

Common causes:

- missing Python dependency
- Docker build failed
- wrong Railway root directory
- service did not use `Dockerfile`

Expected Railway root directory:

```text
ragaib
```

Expected health URL:

```text
https://your-railway-api-url/health
```

## `/health` Works But `total_chunks` Is `0`

The backend deployed, but the vector DB has not been built on Railway.

Run this in Railway:

```bash
sh scripts/railway_index.sh
```

Then check `/health` again. `total_chunks` should be greater than `0`.

## Vercel Page Loads But Submit Fails

Check the **API Base URL** field in the demo page.

It should be your Railway backend URL, for example:

```text
https://your-railway-api-url
```

Do not include:

```text
/eval/live-query
/chat
/health
```

The frontend adds endpoint paths itself.

## Browser Shows A CORS Error

Go to Railway environment variables and set:

```env
ALLOWED_ORIGINS=https://your-vercel-site.vercel.app
```

For preview deployments, use comma-separated origins:

```env
ALLOWED_ORIGINS=https://your-vercel-site.vercel.app,https://your-preview-site.vercel.app
```

After changing Railway env vars, redeploy or restart the Railway service.

## OpenRouter/Auth Errors

If the backend returns an LLM error:

1. Rotate your OpenRouter key.
2. Put the new key in Railway:
   ```env
   OPENROUTER_API_KEY=your_new_key
   ```
3. Make sure the provider/model settings are present:
   ```env
   LLM_PROVIDER=openrouter
   LLM_MODEL=openrouter/free
   JUDGE_PROVIDER=openrouter
   JUDGE_MODEL=openrouter/free
   BASELINE_PROVIDER=openrouter
   BASELINE_MODEL=openrouter/free
   ```
4. Restart Railway.

## First Query Is Slow

This can be normal. The first retrieval/indexing path may load BGE-M3 from the persistent Hugging Face cache.

Make sure Railway has:

```env
HF_HOME=/app/vector_db/huggingface
```

and persistent storage mounted at:

```text
/app/vector_db
```

## Final Verification Command

Run this from `ragaib/` after Railway and Vercel are both live:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_deployment.ps1 `
  -ApiBaseUrl "https://your-railway-api-url" `
  -FrontendOrigin "https://your-vercel-site.vercel.app"
```

If this passes, the deployed demo wiring is healthy.
