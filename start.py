import os
import sys
from pathlib import Path

def main():
    print("🚀 Starting BioAccess on Railway")
    
    # Carregar variáveis de ambiente do .env.local (desenvolvimento local)
    env_local = Path(__file__).parent / ".env.local"
    if env_local.exists():
        print(f"📝 Loading environment from: {env_local}")
        with open(env_local, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())
    
    # Configurar DATABASE_URL a partir do SUPABASE_DB_URL
    if os.getenv("SUPABASE_DB_URL"):
        os.environ["DATABASE_URL"] = os.getenv("SUPABASE_DB_URL")
        print(f"🗄️  Using PostgreSQL database from Railway")
    
    # Mudar para o diretório backend
    backend_dir = Path(__file__).parent / "src" / "backend"
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        sys.exit(1)
    
    # Adicionar o diretório backend ao Python path ANTES de mudar o diretório
    sys.path.insert(0, str(backend_dir))
    
    os.chdir(backend_dir)
    print(f"📁 Working directory: {backend_dir}")
    print(f"🐍 Python version: {sys.version}")
    
    # Configuração para Railway/Cloud
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("PORT", str(os.getenv("PORT", "8000")))
    
    # Inicializar banco de dados
    try:
        print("🗄️  Inicializando banco de dados...")
        from app.config import Base, engine, SessionLocal
        from app.models.user import User
        from app.routers.auth import pwd_context
        
        # Criar tabelas
        print("📋 Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas!")
        
        # Verificar e criar usuários padrão
        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            print(f"✅ Conexão OK - {user_count} usuários")
            
            if user_count == 0:
                print("👤 Criando usuários padrão...")
                default_users = [
                    User(username="ana.luiza", password_hash=pwd_context.hash("senha123"), role="public", clearance=1),
                    User(username="teste1", password_hash=pwd_context.hash("teste123"), role="public", clearance=1),
                    User(username="demo", password_hash=pwd_context.hash("demo123"), role="director", clearance=2),
                    User(username="admin", password_hash=pwd_context.hash("admin123"), role="minister", clearance=3),
                ]
                for user in default_users:
                    db.add(user)
                db.commit()
                print(f"✅ {len(default_users)} usuários criados!")
        except Exception as e:
            print(f"❌ Erro DB: {e}")
            db.rollback()
            raise
        finally:
            db.close()
            
        print("✅ Banco inicializado!")
    except Exception as e:
        print(f"❌ ERRO FATAL: {e}")
        sys.exit(1)
    
    # Executar servidor
    try:
        import uvicorn
        print("🌟 Starting uvicorn server...")
        
        # Configurações para Railway (com TensorFlow/DeepFace)
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            reload=False,
            log_level="info",
            workers=1,
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()