Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)
.\.venv\Scripts\python.exe -m vector_store.indexer
