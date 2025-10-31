#!/usr/bin/env python3
"""
Script único para inicializar o sistema BioAccess
Configura banco, cria usuários padrão e inicia servidor
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Função principal de inicialização"""
    print("🚀 BIOACCESS - SISTEMA DE AUTENTICAÇÃO BIOMÉTRICA")
    print("=" * 60)
    
    # Verificar se está no diretório correto
    backend_dir = Path("src/backend")
    if not backend_dir.exists():
        print("❌ Execute este script a partir da raiz do projeto!")
        sys.exit(1)
    
    # 1. Configurar banco de dados
    print("🗄️ Configurando banco de dados...")
    os.chdir(backend_dir)
    
    try:
        subprocess.run([sys.executable, "init_db.py"], check=True)
        print("✅ Banco configurado com sucesso!")
    except subprocess.CalledProcessError:
        print("⚠️ Erro ao configurar banco - continuando...")
    
    # 2. Criar usuários padrão  
    print("👥 Criando usuários padrão...")
    try:
        subprocess.run([sys.executable, "create_users_supabase.py"], check=True)
        print("✅ Usuários criados com sucesso!")
    except subprocess.CalledProcessError:
        print("⚠️ Usuários já existem - continuando...")
    
    # 3. Iniciar servidor
    print("🌐 Iniciando servidor BioAccess...")
    print("📍 Backend: http://localhost:8001")
    print("📍 API Docs: http://localhost:8001/docs")
    print("📍 Frontend: Execute 'npm run dev' em outro terminal")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "run_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()