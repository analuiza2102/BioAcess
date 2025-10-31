"""Servidor para usar backend real com Supabase"""

import os
import sys
from pathlib import Path

# Definir o diretório de trabalho correto
backend_dir = Path(__file__).parent.resolve()
print(f"🔧 Diretório de trabalho: {backend_dir}")
os.chdir(backend_dir)

# Adicionar o diretório atual ao PYTHONPATH
sys.path.insert(0, str(backend_dir))

# Garantir que o .env seja carregado
from dotenv import load_dotenv
load_dotenv(backend_dir / '.env')

# Verificar se as variáveis estão carregadas
supabase_url = os.getenv('SUPABASE_DB_URL')
jwt_secret = os.getenv('JWT_SECRET')

print(f"🔧 SUPABASE_DB_URL: {'postgresql' in supabase_url if supabase_url else 'NÃO CONFIGURADO'}")
print(f"🔧 JWT_SECRET: {'CONFIGURADO' if jwt_secret else 'NÃO CONFIGURADO'}")

import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando BioAccess Backend Real...")
    print("🔧 Modo DEMO ativo - processamento biométrico simulado")
    print("🗄️ Banco de dados: Supabase PostgreSQL")
    print("🌐 API Docs: http://127.0.0.1:8001/docs")
    
    # Usar string import para permitir reload
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        reload_dirs=[str(backend_dir)],
        log_level="info"
    )