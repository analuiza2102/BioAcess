@echo off
REM Script para rodar o backend BioAccess em desenvolvimento (Windows)

echo 🚀 Iniciando BioAccess Backend...

REM Verifica se venv existe
if not exist "venv" (
    echo ❌ Virtual environment não encontrado!
    echo Execute: python -m venv venv
    exit /b 1
)

REM Ativa venv
call venv\Scripts\activate

REM Verifica se .env existe
if not exist ".env" (
    echo ⚠️  Arquivo .env não encontrado!
    echo Copiando .env.example para .env...
    copy .env.example .env
    echo ✅ Configure o arquivo .env com suas credenciais Supabase
    exit /b 1
)

REM Instala dependências se necessário
if not exist "venv\Scripts\uvicorn.exe" (
    echo 📦 Instalando dependências...
    pip install -r requirements.txt
)

REM Roda servidor
echo ✅ Iniciando servidor em http://localhost:8000
echo 📚 Documentação: http://localhost:8000/docs
uvicorn app.main:app --reload --port 8000
