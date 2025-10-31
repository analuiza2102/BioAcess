#!/bin/bash
# Script para debug do Render - verificar qual arquivo está sendo lido

echo "🔍 Verificando arquivos de requirements no Render..."
echo "📁 Diretório atual:"
pwd
echo ""
echo "📋 Arquivos encontrados:"
ls -la *requirements*
echo ""
echo "🎯 Conteúdo do requirements_render.txt:"
cat requirements_render.txt
echo ""
echo "⚠️ Conteúdo do requirements.txt (se existir):"
if [ -f "requirements.txt" ]; then
    cat requirements.txt
else
    echo "requirements.txt não encontrado"
fi
echo ""
echo "🚀 Iniciando instalação com requirements_render.txt..."
pip install -r requirements_render.txt