Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
    [string]$Dataset = ".\physics_bee_20.csv",
    [int]$TopK = 6,
    [int]$Limit = 0
)

Set-Location (Split-Path -Parent $PSScriptRoot)

$argsList = @("-m", "evaluation.retrieval_eval", "--dataset", $Dataset, "--top-k", "$TopK")
if ($Limit -gt 0) {
    $argsList += @("--limit", "$Limit")
}

.\.venv\Scripts\python.exe @argsList
