# Demo and Deployment Notes

For the detailed production deployment checklist, use:

```text
docs/VERCEL_RAILWAY_DEPLOYMENT.md
```

## Local Demo

Start the API:

```powershell
cd C:\Users\BKAWIN\Desktop\RAG\ragaib
.\.venv\Scripts\python.exe -m uvicorn chat.api:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/demo/
```

The demo lets you:

- edit a homepage description,
- enter a test query,
- choose subject, grade, language, source, and answer type,
- compare RAG vs baseline answers,
- inspect retrieved chunks,
- view judge metrics and winner.

## Live Query API

Endpoint:

```text
POST /eval/live-query
```

Example request:

```json
{
  "message": "What is Newton's second law?",
  "subject": "physics",
  "grade": "M4",
  "preferred_answer_type": "homework-help",
  "language": "EN",
  "top_k": 6
}
```

## Vercel Deployment Strategy

Recommended setup:

- Vercel hosts only the static demo frontend.
- Render or Railway hosts the Python FastAPI backend.

Reason:

- The backend uses Chroma, BGE-M3, sentence-transformers, and a generated vector DB.
- The vector DB is large and persistent.
- Vercel serverless is not a good fit for the full RAG backend.

## Backend Deployment Requirements

Backend needs:

- Python dependencies from `requirements.txt`
- OpenRouter environment variables
- Chroma vector DB
- persistent disk for `vector_db/`

First-time backend setup:

```bash
python -m vector_store.indexer
uvicorn chat.api:app --host 0.0.0.0 --port $PORT
```

## Vercel Frontend Setup

Deploy the `demo/` folder as a static site.

For production, the demo should call the hosted backend URL instead of assuming same-origin localhost. Add or configure an API base URL such as:

```text
https://your-ragaib-api.onrender.com
```

## Safety Note

Do not put `OPENROUTER_API_KEY` in frontend code or Vercel public environment variables. Keep it only on the backend.
