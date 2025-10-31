#!/usr/bin/env python3
"""
Launcher para BioAccess no Railway
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # Mudar para o diretório backend
    backend_dir = Path(__file__).parent / "src" / "backend"
    os.chdir(backend_dir)
    
    print(f"🚀 Starting BioAccess from: {backend_dir}")
    print(f"🐍 Python executable: {sys.executable}")
    
    # Executar o servidor
    try:
        subprocess.run([sys.executable, "run_server.py"], check=True)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
