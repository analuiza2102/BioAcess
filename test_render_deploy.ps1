# Script de teste rápido - Execute após o deploy
# PowerShell

Write-Host "🧪 Testando BioAccess no Render..." -ForegroundColor Cyan

$API = "https://bioacess.onrender.com"
$ORIGIN = "https://bio-acess.vercel.app"

# Teste 1: Health
Write-Host "`n✅ Teste 1: Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$API/health" -Method GET
    Write-Host "Status: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Falhou: $_" -ForegroundColor Red
}

# Teste 2: CORS Preflight
Write-Host "`n✅ Teste 2: CORS Preflight (OPTIONS)" -ForegroundColor Yellow
try {
    $headers = @{
        "Origin" = $ORIGIN
        "Access-Control-Request-Method" = "POST"
        "Access-Control-Request-Headers" = "content-type"
    }
    $response = Invoke-WebRequest -Uri "$API/auth/login" -Method OPTIONS -Headers $headers -UseBasicParsing
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "CORS Origin: $($response.Headers['Access-Control-Allow-Origin'])" -ForegroundColor Green
} catch {
    Write-Host "❌ Falhou: $_" -ForegroundColor Red
}

# Teste 3: Login
Write-Host "`n✅ Teste 3: Login POST" -ForegroundColor Yellow
try {
    $body = @{
        username = "ana.luiza"
        password = "senha123"
    } | ConvertTo-Json

    $headers = @{
        "Content-Type" = "application/json"
        "Origin" = $ORIGIN
    }
    
    $response = Invoke-RestMethod -Uri "$API/auth/login" -Method POST -Body $body -Headers $headers
    Write-Host "Token recebido: $($response.access_token.Substring(0,20))..." -ForegroundColor Green
    Write-Host "Role: $($response.role)" -ForegroundColor Green
} catch {
    Write-Host "❌ Falhou: $_" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host $_.ErrorDetails.Message -ForegroundColor Red
    }
}

Write-Host "`n✅ Testes concluídos!" -ForegroundColor Cyan
