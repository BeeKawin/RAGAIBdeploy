# Command Cheat Sheet

Run all commands from:

```powershell
cd C:\Users\BKAWIN\Desktop\RAG\ragaib
```

## Scripts

Run all tests:

```powershell
.\scripts\test_all.ps1
```

Start API and demo:

```powershell
.\scripts\start_api.ps1
```

Build vector index:

```powershell
.\scripts\build_index.ps1
```

Run retrieval evaluation:

```powershell
.\scripts\eval_retrieval.ps1
```

Run retrieval evaluation with a limit:

```powershell
.\scripts\eval_retrieval.ps1 -Limit 3
```

Run full answer evaluation:

```powershell
.\scripts\eval_answers.ps1
```

Resume full answer evaluation:

```powershell
.\scripts\eval_answers.ps1 -ResumeFrom .\data\eval\results\YOUR_FILE.jsonl
```

## Important URLs

```text
http://127.0.0.1:8000/demo/
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

## Useful Manual Commands

Run all tests directly:

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```

Start API directly:

```powershell
.\.venv\Scripts\python.exe -m uvicorn chat.api:app --host 127.0.0.1 --port 8000
```

Run live query API from PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/eval/live-query" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"message":"What is Newton''s second law?","subject":"physics","grade":"M4","preferred_answer_type":"homework-help","language":"EN","top_k":6}'
```
