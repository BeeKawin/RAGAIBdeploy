Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
    [int]$Port = 8000
)

Set-Location (Split-Path -Parent $PSScriptRoot)
.\.venv\Scripts\python.exe -m uvicorn chat.api:app --host 127.0.0.1 --port $Port
