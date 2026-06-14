# Mentor Presentation Notes

Use this as a short script for explaining the project.

## 1. Problem

Students ask high-school STEM questions in Thai or English. A normal LLM can answer, but it may be ungrounded, inconsistent, or not aligned with the student’s desired answer style.

## 2. Goal

Build a RAG system that:

- retrieves curriculum-relevant context,
- answers in the requested language,
- follows answer-type preferences,
- compares against a baseline LLM,
- evaluates answer quality.

## 3. Data Sources

- OpenStax for English curriculum content.
- SciMath for Thai educational content.
- Internal normalized support lessons for small known coverage gaps.

## 4. Document Pipeline

The data pipeline is:

```text
Scrape → Normalize → Chunk → Embed → Index
```

Normalization is important because OpenStax and SciMath have different structures. The system converts both into one canonical document format before chunking.

## 5. Retrieval

The system uses:

- BGE-M3 embeddings,
- Chroma vector DB,
- metadata filters for subject, grade, source, and language,
- English/Thai source routing,
- fallback retrieval if exact grade/source is sparse.

## 6. Generation

The RAG prompt receives:

- retrieved curriculum context,
- subject and grade,
- target language,
- answer type,
- optional keypoints during dataset evaluation.

Answer types:

- quick answer,
- concept focused,
- homework help,
- exam prep,
- general.

## 7. Evaluation

The answer evaluator scores:

- correctness,
- groundedness,
- completeness,
- clarity,
- type alignment,
- overall band.

The live evaluator compares:

- RAG answer,
- baseline LLM answer,
- retrieved chunks,
- judge scores,
- final winner.

## 8. Demo

The demo website shows the full loop:

```text
User query → Retrieval → RAG answer → Baseline answer → Evaluation → Comparison
```

This is useful for quickly testing whether retrieval improves the final answer.

## 9. Current Strengths

- Clear modular pipeline.
- Multilingual retrieval with BGE-M3.
- Separate retrieval and answer evaluation.
- Live RAG-vs-baseline demo.
- Resume-safe offline evaluation.

## 10. Current Limitations

- Full answer evaluation depends on external LLM judge availability.
- The vector DB is local/persistent and needs careful deployment.
- SciMath scraped text quality can still affect retrieval quality.
- Some subject/topic aliases may need expansion beyond the current datasets.

## 11. Next Improvements

- Deploy frontend on Vercel and backend on Render/Railway.
- Add hosted vector DB or object storage backup for Chroma.
- Improve SciMath scraping quality.
- Add more datasets across physics, chemistry, biology, and mathematics.
- Add dashboard summaries from saved live query evaluations.
