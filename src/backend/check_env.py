#!/usr/bin/env python3
"""
Script para verificar se as configurações do .env estão corretas
"""

import os
import sys
from pathlib import Path

def check_env_config():
    """Verifica configurações do arquivo .env"""
    
    print("🔍 VERIFICANDO CONFIGURAÇÕES DO .env")
    print("=" * 50)
    
    # Carregar .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Arquivo .env carregado")
    except ImportError:
        print("❌ Instale python-dotenv: pip install python-dotenv")
        return False
    
    # 1. Verificar SUPABASE_DB_URL
    db_url = os.getenv('SUPABASE_DB_URL')
    if db_url:
        if db_url.startswith('postgresql://'):
            print("✅ SUPABASE_DB_URL: PostgreSQL configurado")
            # Extrair info básica (sem expor senha)
            parts = db_url.split('@')
            if len(parts) > 1:
                server_info = parts[1].split(':')[0]
                print(f"   📍 Servidor: {server_info}")
        elif db_url.startswith('sqlite://'):
            print("⚠️ SUPABASE_DB_URL: SQLite (desenvolvimento)")
        else:
            print("❌ SUPABASE_DB_URL: Formato inválido")
    else:
        print("❌ SUPABASE_DB_URL: Não configurado")
        return False
    
    # 2. Verificar JWT_SECRET
    jwt_secret = os.getenv('JWT_SECRET')
    if jwt_secret:
        if len(jwt_secret) >= 32:
            print(f"✅ JWT_SECRET: Configurado ({len(jwt_secret)} caracteres)")
        else:
            print(f"⚠️ JWT_SECRET: Muito curto ({len(jwt_secret)}/32 caracteres)")
    else:
        print("❌ JWT_SECRET: Não configurado")
        return False
    
    # 3. Verificar configurações opcionais
    threshold = os.getenv('BIOMETRIC_THRESHOLD', '0.6')
    print(f"🎯 BIOMETRIC_THRESHOLD: {threshold}")
    
    liveness = os.getenv('LIVENESS_ENABLED', 'true')
    print(f"👁️ LIVENESS_ENABLED: {liveness}")
    
    debug = os.getenv('DEBUG', 'false')
    print(f"🐛 DEBUG: {debug}")
    
    port = os.getenv('API_PORT', '8001')
    print(f"🌐 API_PORT: {port}")
    
    print("\n" + "=" * 50)
    print("✅ Configurações verificadas com sucesso!")
    return True

def test_database_connection():
    """Testa conexão com banco de dados"""
    print("\n🗄️ TESTANDO CONEXÃO COM BANCO...")
    
    try:
        from app.db import get_db
        db = next(get_db())
        
        # Testar query simples
        if 'postgresql' in os.getenv('SUPABASE_DB_URL', ''):
            from sqlalchemy import text
            result = db.execute(text("SELECT version()")).fetchone()
            print("✅ Conexão PostgreSQL: OK")
        else:
            result = db.execute("SELECT sqlite_version()").fetchone()
            print("✅ Conexão SQLite: OK")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("💡 Verifique se o Supabase está acessível")
        return False

def main():
    """Função principal"""
    
    # Verificar se está no diretório correto
    if not Path('.env').exists():
        print("❌ Arquivo .env não encontrado!")
        print("💡 Execute este script no diretório src/backend")
        sys.exit(1)
    
    # Verificar configurações
    config_ok = check_env_config()
    
    if config_ok:
        # Testar conexão
        db_ok = test_database_connection()
        
        if db_ok:
            print("\n🎉 TUDO CONFIGURADO CORRETAMENTE!")
            print("🚀 Você pode executar: python run_server.py")
        else:
            print("\n⚠️ Configurações OK, mas problema na conexão DB")
    else:
        print("\n❌ Corrija as configurações do .env primeiro")

if __name__ == "__main__":
    main()