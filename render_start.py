#!/usr/bin/env python3
"""
Render.com launcher para BioAccess
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Starting BioAccess on Render.com")
    
    # Mudar para o diretório backend
    backend_dir = Path(__file__).parent / "src" / "backend"
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        sys.exit(1)
        
    os.chdir(backend_dir)
    print(f"📁 Working directory: {backend_dir}")
    print(f"🐍 Python executable: {sys.executable}")
    
    # Configuração para Render
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("PORT", str(os.getenv("PORT", "10000")))
    
    # Executar servidor
    try:
        import uvicorn
        print("🌟 Starting uvicorn server...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 10000)),
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()