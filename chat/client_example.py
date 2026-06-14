"""
chat/client_example.py
───────────────────────
Example client showing REST + WebSocket usage.
Run after the API is started: uvicorn chat.api:app --port 8000
"""

import asyncio
import json

import httpx
import websockets

BASE_URL = "http://localhost:8000"
WS_URL   = "ws://localhost:8000"


# ── REST: blocking chat ───────────────────────────────────────────────────────

def ask(
    message: str,
    subject: str = None,
    grade: str = None,
    preferred_answer_type: str = None,
):
    payload = {
        "message": message,
        "subject": subject,
        "grade": grade,
    }
    if preferred_answer_type:
        payload["preferred_answer_type"] = preferred_answer_type
    resp = httpx.post(f"{BASE_URL}/chat", json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    print("\n── Answer ──────────────────────────────────────")
    print(data["answer"])
    print("\n── Sources ─────────────────────────────────────")
    for s in data["sources"]:
        print(f"  • [{s['subject']}|{s['grade']}] {s['topic']} › {s['section']}")
        print(f"    {s['url']}")


# ── WebSocket: streaming chat ─────────────────────────────────────────────────

async def ask_stream(
    message: str,
    subject: str = None,
    grade: str = None,
    preferred_answer_type: str = None,
):
    uri = f"{WS_URL}/chat/stream"
    async with websockets.connect(uri) as ws:
        payload = {
            "message": message,
            "subject": subject,
            "grade":   grade,
        }
        if preferred_answer_type:
            payload["preferred_answer_type"] = preferred_answer_type
        await ws.send(json.dumps(payload))
        print("\n── Streaming Answer ─────────────────────────────")
        async for raw in ws:
            try:
                frame = json.loads(raw)
                if frame.get("done"):
                    print("\n\n── Sources ─────────────────────────────────────")
                    for s in frame.get("sources", []):
                        print(f"  • {s['topic']} › {s['section']}")
                    break
                if "error" in frame:
                    print(f"Error: {frame['error']}")
                    break
            except json.JSONDecodeError:
                # Plain text chunk
                print(raw, end="", flush=True)


# ── Health check ──────────────────────────────────────────────────────────────

def health():
    resp = httpx.get(f"{BASE_URL}/health")
    print(json.dumps(resp.json(), indent=2))


# ── Example usage ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Health Check ===")
    health()

    print("\n── Biology: Exam Prep (focused on key concepts) ──────────────────────")
    ask(
        message="What is photosynthesis?",
        subject="biology",
        grade="M4",
        preferred_answer_type="exam-prep",
    )

    print("\n── Biology: Quick Answer (minimal explanation) ─────────────────────")
    ask(
        message="What is photosynthesis?",
        subject="biology",
        grade="M4",
        preferred_answer_type="quick-answer",
    )

    print("\n── Chemistry: Homework Help (step-by-step) ──────────────────────────")
    ask(
        message="How do I solve this equation? H2SO4 + 2NaOH → Na2SO4 + 2H2O",
        subject="chemistry",
        grade="M5",
        preferred_answer_type="homework-help",
    )

    print("\n── Physics: Concept-Focused (explanation & reasoning) ─────────────────")
    ask(
        message="Explain Newton's Second Law",
        subject="physics",
        grade="M4",
        preferred_answer_type="concept-focused",
    )

    print("\n── Chemistry: Default (balanced explanation) ──────────────────────────")
    ask(
        message="Explain titration in simple terms",
        subject="chemistry",
        grade="M5",
    )