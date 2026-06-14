# Chat API Answer Type Configuration - Summary

## Changes Made (June 10, 2026)

### 1. Updated chat/api.py

**ChatRequest Model** - Added optional parameter:
```python
class ChatRequest(BaseModel):
    message: str
    subject: Optional[str] = None
    grade: Optional[str] = None
    top_k: int = 6
    preferred_answer_type: Optional[str] = None  # quick-answer, concept-focused, homework-help, exam-prep
```

**POST /chat Endpoint** - Now passes preferred_answer_type to chain.ask():
```python
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    chain = get_rag_chain()
    try:
        answer = chain.ask(
            req.message,
            subject=req.subject,
            grade=req.grade,
            top_k=req.top_k,
            preferred_answer_type=req.preferred_answer_type,  # NEW
        )
        # ...
```

### 2. Updated chat/client_example.py

**ask() function** - Added preferred_answer_type parameter:
```python
def ask(
    message: str,
    subject: str = None,
    grade: str = None,
    preferred_answer_type: str = None,  # NEW
):
    payload = {
        "message": message,
        "subject": subject,
        "grade": grade,
    }
    if preferred_answer_type:
        payload["preferred_answer_type"] = preferred_answer_type
    # ...
```

**ask_stream() function** - Added preferred_answer_type parameter for WebSocket streaming.

**Example usage section** - Added 5 different examples demonstrating each answer type:
- quick-answer
- homework-help
- concept-focused
- exam-prep
- default (balanced)

### 3. Created CHAT_API_ANSWER_TYPES.py

Comprehensive documentation file including:
- Supported answer types with descriptions
- API endpoint usage examples
- cURL examples
- Python client examples
- Integration notes with evaluation dataset

## Answer Types

| Type | Use Case | Response Style |
|------|----------|---|
| `quick-answer` | Need just the answer | Shortest possible, minimal explanation |
| `concept-focused` | Want understanding | Deep conceptual explanation |
| `homework-help` | Need guidance solving | Step-by-step with formulas |
| `exam-prep` | Studying for test | Concise with key formulas and common mistakes |
| `(default)` | Balanced approach | Standard educational answer |

## Integration with Existing System

✓ **Backend Support**: retrieval/rag_chain.py already had full support
- ask() method accepts preferred_answer_type parameter
- ask_stream() method accepts preferred_answer_type parameter
- System prompt has dedicated Answer-Type Instructions section
- _target_answer_type() function handles normalization

✓ **Evaluation Dataset Alignment**: Answer types match the evaluation dataset "type" column
- quick-answer
- concept-focused
- homework-help
- exam-prep

✓ **Backward Compatibility**: Optional parameter defaults to None (uses "general" in prompt)

## How It Works

1. User sends request with `preferred_answer_type`
2. API passes it to `chain.ask()`
3. RAG chain injects it into system prompt
4. LLM receives specific instructions for that answer type
5. Answer is generated according to style

Example request:
```json
{
  "message": "What is photosynthesis?",
  "subject": "biology",
  "grade": "M4",
  "preferred_answer_type": "exam-prep"
}
```

## Testing

Run the client examples to test different answer types:
```bash
python chat/client_example.py
```

Or use curl to test individual answer types:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is photosynthesis?",
    "subject": "biology",
    "grade": "M4",
    "preferred_answer_type": "quick-answer"
  }'
```
