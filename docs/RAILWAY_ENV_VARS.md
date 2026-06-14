# Railway Environment Variables

Use this when configuring the Railway backend service.

Replace the placeholder values before saving.

```env
LLM_PROVIDER=openrouter
LLM_MODEL=openrouter/free

JUDGE_PROVIDER=openrouter
JUDGE_MODEL=openrouter/free

BASELINE_PROVIDER=openrouter
BASELINE_MODEL=openrouter/free

OPENROUTER_API_KEY=replace_with_rotated_openrouter_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_APP_NAME=RAGAI-B-Demo
OPENROUTER_SITE_URL=https://replace-with-your-vercel-domain.vercel.app

ALLOWED_ORIGINS=https://replace-with-your-vercel-domain.vercel.app

EMBEDDING_MODEL=BAAI/bge-m3
EMBEDDING_DIMENSION=1024
CHROMA_COLLECTION=ragaib_bge_m3_v1
HF_HOME=/app/vector_db/huggingface
```

## Notes

- `OPENROUTER_API_KEY` must be a new rotated key.
- `OPENROUTER_SITE_URL` should match your deployed Vercel site.
- `ALLOWED_ORIGINS` controls browser access from Vercel to Railway.
- For Vercel preview URLs, temporarily add them as comma-separated origins:

```env
ALLOWED_ORIGINS=https://your-main-site.vercel.app,https://your-preview-site.vercel.app
```

## Persistent Storage

Mount Railway persistent storage at:

```text
/app/vector_db
```

That path stores:

- Chroma vector DB
- Hugging Face BGE-M3 cache

After the first successful deploy, run:

```bash
sh scripts/railway_index.sh
```

Then check:

```text
https://your-railway-api-url/health
```

`total_chunks` should be greater than `0`.
