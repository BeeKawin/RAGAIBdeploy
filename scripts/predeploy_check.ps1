Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "Running test suite" -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pytest tests

Write-Host ""
Write-Host "Validating deployment JSON" -ForegroundColor Cyan
python -m json.tool demo\vercel.json | Out-Null
python -m json.tool railway.json | Out-Null
Write-Host "JSON config OK"

Write-Host ""
Write-Host "Parsing PowerShell deployment scripts" -ForegroundColor Cyan
$scripts = @(
    "scripts\check_deployment.ps1",
    "scripts\list_deployment_files.ps1",
    "scripts\show_deployment_diff.ps1",
    "scripts\predeploy_check.ps1"
)

foreach ($script in $scripts) {
    $errors = $null
    $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content $script -Raw), [ref]$errors)
    if ($errors -and $errors.Count -gt 0) {
        throw "PowerShell parse failed for $script"
    }
}
Write-Host "PowerShell scripts OK"

Write-Host ""
Write-Host "Checking GitHub Actions workflow" -ForegroundColor Cyan
$workflow = Join-Path $root ".github\workflows\predeploy.yml"
if (-not (Test-Path $workflow)) {
    throw ".github\workflows\predeploy.yml is missing."
}
$workflowText = Get-Content $workflow -Raw
if ($workflowText -notmatch "python -m pytest tests") {
    throw "GitHub Actions workflow does not run the test suite."
}
if ($workflowText -notmatch "data/normalized") {
    throw "GitHub Actions workflow does not check normalized indexing inputs."
}
Write-Host "GitHub Actions workflow OK"

Write-Host ""
Write-Host "Checking sensitive/generated paths are not staged" -ForegroundColor Cyan
$sensitiveStatus = git status --short -- .env .venv vector_db data\eval\results data\eval\summaries data\eval\live_queries
if ($sensitiveStatus) {
    Write-Host $sensitiveStatus -ForegroundColor Yellow
    throw "Sensitive or generated paths appear in git status. Do not deploy until reviewed."
}
Write-Host "Sensitive/generated paths OK"

Write-Host ""
Write-Host "Checking normalized indexing inputs" -ForegroundColor Cyan
$normalizedDir = Join-Path $root "data\normalized"
if (-not (Test-Path $normalizedDir)) {
    throw "data\normalized is missing. Railway indexing will produce 0 chunks."
}
$normalizedCount = (Get-ChildItem $normalizedDir -Recurse -Filter *.json | Measure-Object).Count
Write-Host "Normalized JSON files: $normalizedCount"
if ($normalizedCount -le 0) {
    throw "No normalized JSON files found. Railway indexing will produce 0 chunks."
}

Write-Host ""
powershell -ExecutionPolicy Bypass -File scripts\list_deployment_files.ps1

Write-Host ""
Write-Host "Predeploy check passed." -ForegroundColor Green
Write-Host "Next: commit selected deployment files, push to GitHub, then deploy Railway before Vercel."
