# Script de preparação para deploy no Vercel
# Execute antes de fazer deploy

Write-Host "🚀 Preparando deploy do Frontend para Vercel..." -ForegroundColor Green

# 1. Verificar Node.js
Write-Host "📦 Verificando Node.js..." -ForegroundColor Yellow
node --version
npm --version

# 2. Instalar dependências
Write-Host "📋 Instalando dependências..." -ForegroundColor Yellow
npm install --legacy-peer-deps

# 3. Testar build
Write-Host "🔨 Testando build..." -ForegroundColor Yellow
npm run build

if ($?) {
    Write-Host "✅ Build do frontend funcionando!" -ForegroundColor Green
    Write-Host "" 
    Write-Host "🎯 Próximos passos:" -ForegroundColor Cyan
    Write-Host "1. Acesse https://vercel.com/dashboard" -ForegroundColor White
    Write-Host "2. Clique em 'New Project'" -ForegroundColor White
    Write-Host "3. Conecte o repositório analuiza2102/BioAcess" -ForegroundColor White
    Write-Host "4. Configure VITE_API_URL com URL do Render" -ForegroundColor White
    Write-Host "5. Deploy!" -ForegroundColor White
} else {
    Write-Host "❌ Erro no build. Verifique as dependências." -ForegroundColor Red
}