#!/usr/bin/env python3
"""
API Chat Answer Type Configuration
===================================

The chat API now supports specifying the preferred answer type via the
'preferred_answer_type' parameter. This allows users to get answers tailored
to their specific learning needs.

SUPPORTED ANSWER TYPES
======================

1. quick-answer
   - Shortest correct answer possible
   - Minimal explanation
   - Immediate final answer
   - Use when: You need just the answer

2. concept-focused
   - Focus on understanding
   - Explain meanings and relationships
   - Explain why concepts work
   - Avoid unnecessary calculations
   - Use when: You want deep conceptual understanding

3. homework-help
   - Step-by-step solution
   - Explain formula selection
   - Show substitutions and calculations clearly
   - Final answer emphasized
   - Use when: You're solving a problem and need guidance

4. exam-prep
   - Focus on revision and exam readiness
   - Highlight important formulas
   - Summarize key concepts
   - Mention common mistakes or frequently tested points
   - Keep explanations concise
   - Use when: You're preparing for an exam

5. (default/general)
   - Balanced educational answer
   - Include enough explanation to understand
   - Avoid excessive detail unless needed
   - Use when: Not specified or unsure

API ENDPOINT USAGE
==================

POST /chat
──────────

Request body:
{
  "message": "What is photosynthesis?",
  "subject": "biology",
  "grade": "M4",
  "preferred_answer_type": "exam-prep",  # Optional
  "top_k": 6
}

Response:
{
  "answer": "... answer tailored to exam-prep style ...",
  "subject": "biology",
  "grade": "M4",
  "sources": [...]
}

EXAMPLES
========

Example 1: Quick Answer
───────────────────────
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is photosynthesis?",
    "subject": "biology",
    "grade": "M4",
    "preferred_answer_type": "quick-answer"
  }'

Expected response: Single sentence or brief definition.


Example 2: Homework Help
────────────────────────
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I calculate pH from [H+]?",
    "subject": "chemistry",
    "grade": "M5",
    "preferred_answer_type": "homework-help"
  }'

Expected response: Step-by-step solution with formula, substitution, and final answer.


Example 3: Exam Prep
────────────────────
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the key laws of thermodynamics?",
    "subject": "physics",
    "grade": "M6",
    "preferred_answer_type": "exam-prep"
  }'

Expected response: Concise summary with key formulas and commonly tested points.


Example 4: Concept-Focused
───────────────────────────
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Why does pressure affect equilibrium?",
    "subject": "chemistry",
    "grade": "M5",
    "preferred_answer_type": "concept-focused"
  }'

Expected response: Detailed explanation of underlying principles and reasoning.


PYTHON CLIENT EXAMPLES
======================

See chat/client_example.py for complete working examples with httpx and asyncio.

Quick example:

  import httpx

  payload = {
      "message": "What is DNA replication?",
      "subject": "biology",
      "grade": "M5",
      "preferred_answer_type": "homework-help",
  }

  resp = httpx.post("http://localhost:8000/chat", json=payload, timeout=60)
  data = resp.json()
  print(data["answer"])


INTEGRATION WITH EVALUATION DATASET
====================================

The answer types come directly from the evaluation dataset schema:
- biology_bee_20.csv
- chemistry_bee_20.csv
- mathematics_bee_20.csv
- physics_bee_20.csv

Field: "type" column in CSV files
Values: quick-answer, concept-focused, homework-help, exam-prep

This ensures consistency between:
✓ Evaluation dataset expectations
✓ API user-facing options
✓ LLM prompt instructions
✓ Answer quality metrics
"""

if __name__ == "__main__":
    print(__doc__)
