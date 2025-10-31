#!/usr/bin/env python3
"""
Arquivo de inicialização para Railway
"""
import os
import sys
from pathlib import Path

# Adicionar src/backend ao path
backend_path = Path(__file__).parent / "src" / "backend"
sys.path.insert(0, str(backend_path))

# Importar e executar
os.chdir(backend_path)

if __name__ == "__main__":
    import uvicorn
    
    # Configuração para Railway
    port = int(os.environ.get("PORT", 8001))
    host = "0.0.0.0"
    
    print(f"🚀 Iniciando servidor na porta {port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )