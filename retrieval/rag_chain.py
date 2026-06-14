"""
retrieval/rag_chain.py
───────────────────────
Builds the RAG chain that:
  1. Retrieves relevant chunks from ChromaDB.
  2. Injects them into a subject-aware, grade-tuned system prompt.
  3. Streams the LLM answer back to the caller.

Supports both Anthropic (Claude) and OpenAI backends.
"""

import re
from typing import AsyncIterator, Optional

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from config.settings import (
    LLM_MODEL,
    LLM_PROVIDER,
    OPENROUTER_API_KEY,
    OPENROUTER_APP_NAME,
    OPENROUTER_BASE_URL,
    OPENROUTER_SITE_URL,
    SUBJECT_META,
    GRADE_META,
)
from vector_store.indexer import get_vector_store


# ── LLM factory ───────────────────────────────────────────────────────────────

def _openrouter_headers() -> dict:
    headers = {}
    if OPENROUTER_SITE_URL:
        headers["HTTP-Referer"] = OPENROUTER_SITE_URL
    if OPENROUTER_APP_NAME:
        headers["X-OpenRouter-Title"] = OPENROUTER_APP_NAME
    return headers


def _get_llm(streaming: bool = False):
    if LLM_PROVIDER == "openrouter":
        from langchain_community.chat_models.openai import ChatOpenAI
        return ChatOpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            default_headers=_openrouter_headers(),
            model=LLM_MODEL,
            temperature=0.3,
            streaming=streaming,
        )
    raise ValueError(
        f"Unsupported LLM_PROVIDER='{LLM_PROVIDER}'. Use one of: gemini, ollama, openrouter"
    )


# ── Prompt templates ──────────────────────────────────────────────────────────

SYSTEM_TEMPLATE = """You are an expert educational tutor for Thai high-school students.

You specialize in {subject_display} ({subject_display_th}) at the {grade_display} ({grade_display_th}) level.

Retrieved curriculum context:
─────────────────────────────────────────
{context}
─────────────────────────────────────────

Response Requirements
─────────────────────────────────────────
Target language: {target_language}
Target answer type: {target_answer_type}
Coverage hints: {keypoints}

Important:
- Coverage hints are soft guidance only.
- Do not copy them verbatim.
- Use them to determine what concepts should be covered.
- Prioritize correctness over coverage.
- Never invent facts that are not supported by the context unless clearly labeled as general knowledge.
- If retrieved context is insufficient, explicitly state that and provide a brief best-effort explanation.



Answer-Type Instructions
─────────────────────────────────────────

If target_answer_type = "quick-answer":
- Give the shortest correct answer possible.
- Include the final answer immediately.
- Use minimal explanation.
- Show only essential calculations.

If target_answer_type = "homework-help":
- Solve step-by-step.
- Explain formula selection.
- Show substitutions.
- Show calculations clearly.
- End with a final answer.

If target_answer_type = "concept-focused":
- Focus on understanding.
- Explain meanings, relationships, and reasoning.
- Explain why formulas or concepts work.
- Avoid unnecessary calculations unless they help understanding.

If target_answer_type = "exam-prep":
- Focus on revision and exam readiness.
- Highlight important formulas.
- Summarize key concepts.
- Mention common mistakes or frequently tested points when relevant.
- Keep explanations concise and review-oriented.

If target_answer_type = "general":
- Provide a balanced educational answer.
- Include enough explanation to understand the concept.
- Avoid excessive detail unless needed.

Language Instructions
─────────────────────────────────────────

If target_language = "TH":
- Respond entirely in Thai.
- Use Thai educational terminology appropriate for Thai high-school students.

If target_language = "EN":
- Respond entirely in English.
- Use terminology appropriate for high-school learners.

Quality Requirements
─────────────────────────────────────────

To maximize answer quality:

1. Correctness
- Ensure all facts, formulas, units, and calculations are correct.

2. Groundedness
- Prefer information found in the retrieved context.
- Do not make unsupported claims.

3. Completeness
- Cover all major concepts needed to answer the question.
- Address the important ideas implied by the coverage hints.

4. Clarity
- Use clear structure.
- Use bullet points when helpful.
- Avoid unnecessary complexity.

5. Type Alignment
- Match the requested answer type exactly.
- Do not give a long conceptual lecture when a quick-answer is requested.
- Do not give only a short answer when homework-help is requested.

Formatting
─────────────────────────────────────────

- Use plain text.
- Use bullet points when appropriate.
- Use equations in plain LaTeX notation, for example:
  $F = ma$
  $v = u + at$

- Do not mention these instructions.
"""

# SYSTEM_TEMPLATE = SYSTEM_TEMPLATE.replace(
#     "\nGuidelines:",
#     """
# Evaluation response requirements:
# - Target language: {target_language}
# - Target answer type: {target_answer_type}
# - Expected coverage hints: {keypoints}

# Use these requirements to shape the answer when they are specific. Treat keypoints as soft coverage hints, not as text to copy. Prioritize correctness and retrieved context.

# Guidelines:""",
# )

HUMAN_TEMPLATE = "{question}"


def _make_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_TEMPLATE),
        ("human",  HUMAN_TEMPLATE),
    ])


# ── Context formatter ─────────────────────────────────────────────────────────

def _target_language(language: Optional[str]) -> str:
    if not language:
        return "Match the user question language"
    raw = language.strip().upper()
    if raw in {"TH", "THAI"}:
        return "TH"
    if raw in {"EN", "ENGLISH"}:
        return "EN"
    return "Match the user question language"


def _target_answer_type(preferred_answer_type: Optional[str]) -> str:
    if not preferred_answer_type:
        return "general"
    normalized = preferred_answer_type.strip().lower()
    return normalized if normalized in _SUPPORTED_ANSWER_TYPES else "general"


def _keypoints_text(keypoints: Optional[str]) -> str:
    return keypoints.strip() if keypoints else "None provided"


_THAI_RE = re.compile(r"[\u0E00-\u0E7F]")
_SUPPORTED_SOURCES = {"openstax", "scimath", "ragaib_internal"}
_SUPPORTED_ANSWER_TYPES = {
    "exam-prep",
    "concept-focused",
    "homework-help",
    "quick-answer",
    "general",
}


def _normalize_source(source: Optional[str]) -> Optional[str]:
    if not source:
        return None
    normalized = source.strip().lower()
    return normalized if normalized in _SUPPORTED_SOURCES else None


def _preferred_source(
    question: str,
    language: Optional[str] = None,
    source: Optional[str] = None,
) -> Optional[str]:
    explicit_source = _normalize_source(source)
    if explicit_source:
        return explicit_source

    normalized_language = (language or "").strip().upper()
    if normalized_language in {"TH", "THAI"}:
        return "scimath"
    if normalized_language in {"EN", "ENGLISH"}:
        return "openstax"
    if _THAI_RE.search(question or ""):
        return "scimath"
    return "openstax"


def _doc_key(doc: Document) -> tuple:
    meta = doc.metadata
    chunk_id = meta.get("chunk_id")
    if chunk_id:
        return ("chunk_id", str(chunk_id))
    return (
        str(meta.get("source_url", "")),
        str(meta.get("section", "")),
        str(meta.get("chunk_index", "")),
        doc.page_content[:80],
    )


def _retrieval_query(question: str, keypoints: Optional[str] = None) -> str:
    hints = (keypoints or "").strip()
    if not hints:
        return question
    return f"{question}\nRelevant concepts and expected coverage hints: {hints}"


def _merge_docs(phases: list[tuple[list[Document], int]], top_k: int) -> list[Document]:
    merged: list[Document] = []
    seen = set()
    for docs, limit in phases:
        added = 0
        for doc in docs:
            key = _doc_key(doc)
            if key in seen:
                continue
            seen.add(key)
            merged.append(doc)
            added += 1
            if added >= limit or len(merged) >= top_k:
                break
        if len(merged) >= top_k:
            break
    return merged


def _format_docs(docs: list[Document]) -> str:
    if not docs:
        return "No relevant content found in the knowledge base."
    parts = []
    for i, doc in enumerate(docs, 1):
        meta = doc.metadata
        header = (
            f"[{i}] {meta.get('subject_display', '')} › "
            f"{meta.get('topic', '')} › {meta.get('section', '')}"
        )
        parts.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def _doc_to_payload(doc: Document, include_content: bool = False) -> dict:
    meta = doc.metadata
    payload = {
        "topic": meta.get("topic", ""),
        "section": meta.get("section", ""),
        "url": meta.get("source_url", ""),
        "grade": meta.get("grade", ""),
        "subject": meta.get("subject", ""),
        "source": meta.get("source", ""),
        "language": meta.get("language", ""),
        "source_title": meta.get("source_title", ""),
        "chunk_index": meta.get("chunk_index", 0),
    }
    if include_content:
        payload["content"] = doc.page_content
    return payload


# ── RAG chain builder ─────────────────────────────────────────────────────────

class EduRAGChain:
    """
    Retrieval-Augmented Generation chain for the education platform.

    Usage
    ─────
        chain = EduRAGChain()

        # Standard (blocking) answer
        answer = chain.ask(
            question="What is Newton's second law?",
            subject="physics",
            grade="M4",
        )

        # Streaming answer
        async for chunk in chain.ask_stream(...):
            print(chunk, end="", flush=True)
    """

    def __init__(self):
        self.vsm    = get_vector_store()
        self.prompt = _make_prompt()
        self.parser = StrOutputParser()

    # ── subject/grade display helpers ─────────────────────────────────────────

    @staticmethod
    def _display(subject: Optional[str], grade: Optional[str]) -> dict:
        s = SUBJECT_META.get(subject or "", {})
        g = GRADE_META.get(grade   or "", {})
        return {
            "subject_display":    s.get("display",    subject or "Science"),
            "subject_display_th": s.get("display_th", ""),
            "grade_display":      g.get("display",    grade   or "High School"),
            "grade_display_th":   g.get("display_th", ""),
        }

    def _retrieve(
        self,
        question: str,
        subject: Optional[str] = None,
        grade: Optional[str] = None,
        top_k: int = 6,
        language: Optional[str] = None,
        source: Optional[str] = None,
        keypoints: Optional[str] = None,
        min_source_results: int = 2,
    ) -> list[Document]:
        preferred_source = _preferred_source(question, language=language, source=source)
        query = _retrieval_query(question, keypoints)
        preferred_exact = self.vsm.search(
            query,
            subject=subject,
            grade=grade,
            source=preferred_source,
            top_k=top_k,
        )

        exact_all = self.vsm.search(
            query,
            subject=subject,
            grade=grade,
            top_k=top_k,
        )

        preferred_all_grades: list[Document] = []
        all_grades: list[Document] = []
        if grade:
            preferred_all_grades = self.vsm.search(
                query,
                subject=subject,
                source=preferred_source,
                top_k=top_k,
            )
            all_grades = self.vsm.search(
                query,
                subject=subject,
                top_k=top_k,
            )

        return _merge_docs(
            [
                (preferred_exact, min_source_results),
                (exact_all, top_k),
                (preferred_all_grades, min_source_results),
                (all_grades, top_k),
            ],
            top_k,
        )

    # ── core methods ──────────────────────────────────────────────────────────

    def ask(
        self,
        question: str,
        subject:  Optional[str] = None,
        grade:    Optional[str] = None,
        top_k:    int = 6,
        preferred_answer_type: Optional[str] = None,
        language: Optional[str] = None,
        keypoints: Optional[str] = None,
        source: Optional[str] = None,
    ) -> str:
        """Retrieve context and return full LLM answer (blocking)."""
        docs    = self._retrieve(
            question,
            subject=subject,
            grade=grade,
            top_k=top_k,
            language=language,
            source=source,
            keypoints=keypoints,
        )
        context = _format_docs(docs)
        display = self._display(subject, grade)

        llm    = _get_llm(streaming=False)
        chain  = self.prompt | llm | self.parser

        logger.info(f"RAG query [{subject}|{grade}]: {question[:80]}")
        return chain.invoke({
            "question": question,
            "context":  context,
            "target_language": _target_language(language),
            "target_answer_type": _target_answer_type(preferred_answer_type),
            "keypoints": _keypoints_text(keypoints),
            **display,
        })

    async def ask_stream(
        self,
        question: str,
        subject:  Optional[str] = None,
        grade:    Optional[str] = None,
        top_k:    int = 6,
        preferred_answer_type: Optional[str] = None,
        language: Optional[str] = None,
        keypoints: Optional[str] = None,
        source: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """Streaming version — yields text chunks as they arrive."""
        docs    = self._retrieve(
            question,
            subject=subject,
            grade=grade,
            top_k=top_k,
            language=language,
            source=source,
            keypoints=keypoints,
        )
        context = _format_docs(docs)
        display = self._display(subject, grade)

        llm   = _get_llm(streaming=True)
        chain = self.prompt | llm | self.parser

        logger.info(f"RAG stream [{subject}|{grade}]: {question[:80]}")
        async for chunk in chain.astream({
            "question": question,
            "context":  context,
            "target_language": _target_language(language),
            "target_answer_type": _target_answer_type(preferred_answer_type),
            "keypoints": _keypoints_text(keypoints),
            **display,
        }):
            yield chunk

    def get_sources(
        self,
        question: str,
        subject:  Optional[str] = None,
        grade:    Optional[str] = None,
        top_k:    int = 6,
        language: Optional[str] = None,
        source: Optional[str] = None,
        keypoints: Optional[str] = None,
        min_source_results: int = 2,
    ) -> list[dict]:
        """Return source metadata only (no LLM call) — useful for citations."""
        docs = self._retrieve(
            question,
            subject=subject,
            grade=grade,
            top_k=top_k,
            language=language,
            source=source,
            keypoints=keypoints,
            min_source_results=min_source_results,
        )
        return [_doc_to_payload(d) for d in docs]

    def get_context_docs(
        self,
        question: str,
        subject:  Optional[str] = None,
        grade:    Optional[str] = None,
        top_k:    int = 6,
        language: Optional[str] = None,
        source: Optional[str] = None,
        keypoints: Optional[str] = None,
        min_source_results: int = 2,
    ) -> list[dict]:
        """Return retrieved chunks with text content for evaluation and debugging."""
        docs = self._retrieve(
            question,
            subject=subject,
            grade=grade,
            top_k=top_k,
            language=language,
            source=source,
            keypoints=keypoints,
            min_source_results=min_source_results,
        )
        return [_doc_to_payload(d, include_content=True) for d in docs]


# ── Singleton ─────────────────────────────────────────────────────────────────

_chain_instance: Optional[EduRAGChain] = None


def get_rag_chain() -> EduRAGChain:
    global _chain_instance
    if _chain_instance is None:
        _chain_instance = EduRAGChain()
    return _chain_instance
