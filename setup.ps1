# Script de Setup do BioAccess
# Executa: .\setup.ps1

Write-Host "🚀 Configurando projeto BioAccess..." -ForegroundColor Green

# 1. Setup Python Backend
Write-Host "📦 Configurando Python Backend..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Remove-Item -Recurse -Force "venv"
}

python -m venv venv
.\venv\Scripts\Activate.ps1

Write-Host "📋 Instalando dependências Python..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# 2. Setup Frontend
Write-Host "🌐 Configurando Frontend..." -ForegroundColor Yellow
if (!(Test-Path "node_modules")) {
    npm install --legacy-peer-deps
}

# 3. Build Frontend
Write-Host "🔨 Fazendo build do Frontend..." -ForegroundColor Yellow
npm run build

# 4. Teste rápido do backend
Write-Host "🧪 Testando importações Python..." -ForegroundColor Yellow
python -c "import fastapi, tensorflow, deepface; print('✅ Dependências OK')"

Write-Host "✅ Setup concluído com sucesso!" -ForegroundColor Green
Write-Host "Para executar:" -ForegroundColor Cyan
Write-Host "  Backend: .\venv\Scripts\Activate.ps1 && python src/backend/run_server.py" -ForegroundColor White
Write-Host "  Frontend: npm run dev" -ForegroundColor White