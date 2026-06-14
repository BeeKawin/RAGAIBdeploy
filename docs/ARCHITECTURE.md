# Architecture Overview

## System Goal

RAGAI-B answers Thai high-school STEM questions with curriculum-grounded context. It is designed to compare a RAG answer against a baseline LLM answer and evaluate whether retrieval improves correctness, groundedness, completeness, clarity, and answer-type alignment.

## End-to-End Flow

```text
Raw sources
  OpenStax / SciMath
      ↓
Scrapers
  scraper/openstax_scraper.py
  scraper/scimath_scraper.py
      ↓
Raw JSON
  data/raw/
      ↓
Document normalization
  embeddings/document_normalizer.py
      ↓
Normalized JSON
  data/normalized/
      ↓
Chunking and metadata enrichment
  embeddings/document_processor.py
      ↓
BGE-M3 embeddings + Chroma
  vector_store/indexer.py
      ↓
Retrieval + source routing
  retrieval/rag_chain.py
      ↓
FastAPI app
  chat/api.py
      ↓
Demo UI and evaluation
  demo/
  evaluation/
```

## Core Subsystems

### Document Pipeline

The document pipeline keeps scraped source data separate from normalized documents. Normalized files use a shared schema for OpenStax, SciMath, and internal support lessons. This makes chunking and indexing predictable.

Important outputs:

- `data/raw/`: untouched scraper output.
- `data/normalized/`: validated canonical documents.
- `data/processed/`: processed/chunked artifacts if generated.

### Vector Store

The vector DB uses Chroma with `BAAI/bge-m3` embeddings. BGE-M3 was chosen because it handles multilingual Thai/English STEM retrieval better than the earlier MiniLM-style embedding setup.

Important settings:

- `EMBEDDING_MODEL=BAAI/bge-m3`
- `EMBEDDING_DIMENSION=1024`
- `CHROMA_COLLECTION=ragaib_bge_m3_v1`

### Retrieval and RAG

`retrieval/rag_chain.py` handles:

- Language routing:
  - English queries prefer OpenStax.
  - Thai queries prefer SciMath.
- Source filtering:
  - `source=openstax`
  - `source=scimath`
  - fallback to all sources when needed.
- Soft grade fallback:
  - exact grade first,
  - all grades second if exact grade retrieval is sparse.
- Prompt shaping:
  - language,
  - answer type,
  - keypoints during dataset evaluation.

### Evaluation

There are three evaluation paths:

- `evaluation/retrieval_eval.py`: checks whether retrieval returns relevant topics.
- `evaluation/run_eval.py`: offline dataset answer evaluation.
- `evaluation/live_query_eval.py`: live RAG-vs-baseline comparison for manually typed queries.

### Demo Website

The demo lives in `demo/` and is mounted by FastAPI at:

```text
/demo/
```

It calls:

```text
POST /eval/live-query
```

and displays:

- RAG answer,
- baseline answer,
- retrieved chunks,
- score metrics,
- final comparison.

## Why The Repo Is Organized This Way

The project keeps each stage separate so it is easy to explain:

1. Source acquisition.
2. Document cleaning.
3. Chunking.
4. Embedding and indexing.
5. Retrieval.
6. Answer generation.
7. Evaluation.
8. Demo/deployment.

This separation is also useful for debugging. Bad answers can usually be traced to one of three places: missing source documents, bad retrieval, or weak generation/evaluation.
