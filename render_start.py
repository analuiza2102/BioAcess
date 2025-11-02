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
    
    # Adicionar o diretório backend ao Python path
    sys.path.insert(0, str(backend_dir))
    
    # Inicializar banco de dados
    try:
        print("🗄️  Inicializando banco de dados...")
        from app.db import Base, engine, SessionLocal
        from app.models import User
        from app.security import pwd_context
        
        # Criar tabelas
        print("📋 Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar conexão
        db = SessionLocal()
        try:
            # Testar query simples
            user_count = db.query(User).count()
            print(f"✅ Conexão com banco OK - {user_count} usuários existentes")
            
            # Criar usuários padrão se não existirem
            if user_count == 0:
                print("👤 Criando usuários padrão...")
                default_users = [
                    User(username="ana.luiza", password_hash=pwd_context.hash("senha123"), role="public", clearance=1),
                    User(username="teste1", password_hash=pwd_context.hash("teste123"), role="public", clearance=1),
                    User(username="diretor.silva", password_hash=pwd_context.hash("diretor2024"), role="director", clearance=2),
                    User(username="ministro.ambiente", password_hash=pwd_context.hash("ministro2024"), role="minister", clearance=3),
                ]
                for user in default_users:
                    db.add(user)
                db.commit()
                print(f"✅ {len(default_users)} usuários criados!")
            else:
                print("✅ Usuários já existem no banco!")
        except Exception as e:
            print(f"❌ Erro ao verificar/criar usuários: {e}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise
        finally:
            db.close()
            
        print("✅ Banco de dados inicializado!")
    except Exception as e:
        print(f"❌ ERRO FATAL ao inicializar banco de dados: {e}")
        import traceback
        traceback.print_exc()
        print("⚠️  Servidor NÃO será iniciado devido a erro no banco de dados")
        sys.exit(1)
    
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
        import traceback
        traceback.print_exc()
        sys.exit(1)
        sys.exit(1)

if __name__ == "__main__":
    main()