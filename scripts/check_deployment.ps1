param(
    [Parameter(Mandatory = $true)]
    [string]$ApiBaseUrl,

    [Parameter(Mandatory = $false)]
    [string]$FrontendOrigin = "",

    [Parameter(Mandatory = $false)]
    [int]$TopK = 3
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$api = $ApiBaseUrl.TrimEnd("/")
if (-not $api.StartsWith("http")) {
    throw "ApiBaseUrl must include http:// or https://"
}

Write-Host "Checking Railway API: $api" -ForegroundColor Cyan

$health = Invoke-RestMethod -Method Get -Uri "$api/health"
Write-Host "Health status: $($health.status)"
Write-Host "Collection: $($health.vector_store.collection)"
Write-Host "Embedding: $($health.vector_store.embedding_model)"
Write-Host "Chunks: $($health.vector_store.total_chunks)"

if ([int]$health.vector_store.total_chunks -le 0) {
    throw "Vector DB has 0 chunks. Run this on Railway: python -m vector_store.indexer"
}

if ($FrontendOrigin.Trim()) {
    Write-Host "Checking CORS preflight from $FrontendOrigin" -ForegroundColor Cyan
    $corsHeaders = @{
        Origin = $FrontendOrigin.TrimEnd("/")
        "Access-Control-Request-Method" = "POST"
        "Access-Control-Request-Headers" = "content-type"
    }
    $cors = Invoke-WebRequest -Method Options -Uri "$api/eval/live-query" -Headers $corsHeaders
    $allowOrigin = $cors.Headers["access-control-allow-origin"]
    Write-Host "CORS allow-origin: $allowOrigin"
    if (-not $allowOrigin) {
        throw "CORS preflight did not return access-control-allow-origin. Check Railway ALLOWED_ORIGINS."
    }
}

Write-Host "Checking live query endpoint" -ForegroundColor Cyan
$body = @{
    message = "What is Newton's second law?"
    subject = "physics"
    grade = "M4"
    language = "EN"
    preferred_answer_type = "homework-help"
    top_k = $TopK
} | ConvertTo-Json

$result = Invoke-RestMethod `
    -Method Post `
    -Uri "$api/eval/live-query" `
    -ContentType "application/json" `
    -Body $body

Write-Host "Winner: $($result.winner)"
Write-Host "RAG band: $($result.rag_scores.overall_band)"
Write-Host "Baseline band: $($result.baseline_scores.overall_band)"
Write-Host "Sources returned: $($result.retrieved_sources.Count)"

if (-not $result.rag_answer -or -not $result.baseline_answer) {
    throw "Live query response is missing one or both answers."
}

Write-Host "Deployment check passed." -ForegroundColor Green
