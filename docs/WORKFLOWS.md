# Workflow Guide

This guide explains the main project workflows in the order you can present them.

## 1. Environment Setup

From the project directory:

```powershell
cd C:\Users\BKAWIN\Desktop\RAG\ragaib
.\.venv\Scripts\python.exe -m pytest tests
```

The `.env` file controls the LLM provider, judge provider, OpenRouter key, embedding model, and collection name.

Important environment values:

```env
LLM_PROVIDER=openrouter
LLM_MODEL=openrouter/free
JUDGE_PROVIDER=openrouter
JUDGE_MODEL=openrouter/free
BASELINE_PROVIDER=openrouter
BASELINE_MODEL=openrouter/free
EMBEDDING_MODEL=BAAI/bge-m3
EMBEDDING_DIMENSION=1024
CHROMA_COLLECTION=ragaib_bge_m3_v1
```

## 2. Scrape Sources

OpenStax:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py --site openstax --force-scrape
```

SciMath:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py --site scimath --force-scrape
```

For normal development, skip scraping if raw files already exist:

```powershell
.\.venv\Scripts\python.exe run_pipeline.py --skip-scrape
```

## 3. Normalize Documents

Normalization is included in `run_pipeline.py` unless `--skip-normalize` is passed.

Standalone concept:

```text
raw scraper JSON → normalized canonical JSON
```

Normalized documents live in:

```text
data/normalized/
```

## 4. Process and Index Documents

Build or refresh the Chroma index:

```powershell
.\.venv\Scripts\python.exe -m vector_store.indexer
```

The vector DB lives in:

```text
vector_db/
```

This folder is intentionally gitignored because it is generated and large.

## 5. Start The API

```powershell
.\.venv\Scripts\python.exe -m uvicorn chat.api:app --host 127.0.0.1 --port 8000
```

Useful URLs:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
http://127.0.0.1:8000/demo/
```

## 6. Test Live Query Evaluation

Use the demo website or call the API:

```powershell
curl -X POST http://127.0.0.1:8000/eval/live-query `
  -H "Content-Type: application/json" `
  -d "{\"message\":\"What is Newton's second law?\",\"subject\":\"physics\",\"grade\":\"M4\",\"preferred_answer_type\":\"homework-help\",\"language\":\"EN\",\"top_k\":6}"
```

The response includes:

- `rag_answer`
- `baseline_answer`
- `retrieved_sources`
- `rag_scores`
- `baseline_scores`
- `winner`
- `comparison_rationale`

Live query artifacts are saved in:

```text
data/eval/live_queries/
```

## 7. Run Evaluation Dataset

Retrieval-only evaluation:

```powershell
.\.venv\Scripts\python.exe -m evaluation.retrieval_eval --dataset .\physics_bee_20.csv --top-k 6
```

Full answer evaluation:

```powershell
.\.venv\Scripts\python.exe -m evaluation.run_eval --dataset .\physics_bee_20.csv
```

Resume interrupted evaluation:

```powershell
.\.venv\Scripts\python.exe -m evaluation.run_eval --dataset .\physics_bee_20.csv --resume-from .\data\eval\results\YOUR_FILE.jsonl
```

## 8. Run Tests

All tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```

Focused tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_live_query_eval.py
.\.venv\Scripts\python.exe -m pytest tests\test_source_routing.py
.\.venv\Scripts\python.exe -m pytest tests\test_scoring.py
```
