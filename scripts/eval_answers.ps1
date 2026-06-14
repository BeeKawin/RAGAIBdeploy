Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
    [string]$Dataset = ".\physics_bee_20.csv",
    [int]$Limit = 0,
    [string]$ResumeFrom = ""
)

Set-Location (Split-Path -Parent $PSScriptRoot)

$argsList = @("-m", "evaluation.run_eval", "--dataset", $Dataset)
if ($Limit -gt 0) {
    $argsList += @("--limit", "$Limit")
}
if ($ResumeFrom.Trim()) {
    $argsList += @("--resume-from", $ResumeFrom)
}

.\.venv\Scripts\python.exe @argsList
