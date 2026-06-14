Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$files = @(
    ".dockerignore",
    ".env.example",
    ".github/workflows/predeploy.yml",
    ".gitattributes",
    "Dockerfile",
    "README.md",
    "railway.json",
    "chat/api.py",
    "config/settings.py",
    "demo/app.js",
    "demo/config.js",
    "demo/index.html",
    "demo/styles.css",
    "demo/vercel.json",
    "docs/DEMO_AND_DEPLOYMENT.md",
    "docs/DEPLOYMENT_HANDOFF.md",
    "docs/DEPLOYMENT_FILE_MANIFEST.md",
    "docs/DEPLOYMENT_STATUS_CHECKLIST.md",
    "docs/DEPLOYMENT_TROUBLESHOOTING.md",
    "docs/GIT_DEPLOYMENT_WORKFLOW.md",
    "docs/RAILWAY_ENV_VARS.md",
    "docs/VERCEL_SETUP.md",
    "docs/VERCEL_RAILWAY_DEPLOYMENT.md",
    "scripts/check_deployment.ps1",
    "scripts/list_deployment_files.ps1",
    "scripts/predeploy_check.ps1",
    "scripts/railway_index.sh",
    "scripts/show_deployment_diff.ps1",
    "tests/test_demo_site.py",
    "tests/test_source_routing.py",
    "vector_store/indexer.py"
)

Write-Host "Deployment-related files:" -ForegroundColor Cyan
foreach ($file in $files) {
    $path = Join-Path $root $file
    if (Test-Path $path) {
        Write-Host "  $file"
    } else {
        Write-Host "  MISSING: $file" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Suggested selective staging command:" -ForegroundColor Cyan
Write-Host "git add " -NoNewline
Write-Host ($files -join " ")
