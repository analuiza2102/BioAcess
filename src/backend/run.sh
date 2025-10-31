#!/bin/bash

# Script para rodar o backend BioAccess em desenvolvimento

echo "🚀 Iniciando BioAccess Backend..."

# Verifica se venv existe
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment não encontrado!"
    echo "Execute: python -m venv venv"
    exit 1
fi

# Ativa venv
source venv/bin/activate

# Verifica se .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "Copiando .env.example para .env..."
    cp .env.example .env
    echo "✅ Configure o arquivo .env com suas credenciais Supabase"
    exit 1
fi

# Instala dependências se necessário
if [ ! -f "venv/bin/uvicorn" ]; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
fi

# Roda servidor
echo "✅ Iniciando servidor em http://localhost:8000"
echo "📚 Documentação: http://localhost:8000/docs"
uvicorn app.main:app --reload --port 8000
