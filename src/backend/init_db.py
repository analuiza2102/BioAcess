"""Script para inicializar o banco de dados com usuários de exemplo"""

from sqlalchemy.orm import Session
from app.db import engine, Base, SessionLocal
from app.models import User
from app.security import pwd_context

def create_tables():
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas no banco de dados")

def create_sample_users():
    """Cria usuários de exemplo para teste"""
    db = SessionLocal()
    
    # Usuários de exemplo para teste do sistema
    sample_users = [
        {
            "username": "ana.luiza",
            "password": "senha123",
            "role": "public",
            "clearance": 1,
            "description": "Acesso público - funcionária padrão"
        },
        {
            "username": "diretor.silva",
            "password": "diretor2024",
            "role": "director", 
            "clearance": 2,
            "description": "Diretor de Divisão - relatórios regionais"
        },
        {
            "username": "ministro.ambiente",
            "password": "ministro2024", 
            "role": "minister",
            "clearance": 3,
            "description": "Ministro do Meio Ambiente - acesso total"
        },
        {
            "username": "fiscal.gomes",
            "password": "fiscal123",
            "role": "director",
            "clearance": 2, 
            "description": "Fiscal ambiental - monitoramento regional"
        },
        {
            "username": "analista.santos",
            "password": "analista123",
            "role": "public",
            "clearance": 1,
            "description": "Analista ambiental - dados públicos"
        }
    ]
    
    try:
        for user_data in sample_users:
            # Verifica se usuário já existe
            existing = db.query(User).filter(User.username == user_data["username"]).first()
            if existing:
                print(f"⚠️  Usuário {user_data['username']} já existe, pulando...")
                continue
            
            # Hash da senha (bcrypt tem limite de 72 bytes)
            password = user_data["password"][:72]  # Trunca senha se necessário
            password_hash = pwd_context.hash(password)
            
            # Cria usuário
            user = User(
                username=user_data["username"],
                role=user_data["role"],
                clearance=user_data["clearance"],
                password_hash=password_hash
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            print(f"✅ Criado usuário: {user_data['username']} (clearance {user_data['clearance']}) - {user_data['description']}")
        
        print("\n🎉 Usuários de exemplo criados com sucesso!")
        print("\n📝 CREDENCIAIS PARA TESTE:")
        print("┌─────────────────────┬──────────────┬───────────┬─────────────────────────────────┐")
        print("│ Usuário             │ Senha        │ Clearance │ Descrição                       │")
        print("├─────────────────────┼──────────────┼───────────┼─────────────────────────────────┤")
        for user_data in sample_users:
            print(f"│ {user_data['username']:<19} │ {user_data['password']:<12} │ Nível {user_data['clearance']}   │ {user_data['description']:<31} │")
        print("└─────────────────────┴──────────────┴───────────┴─────────────────────────────────┘")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuários: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal para inicializar o banco"""
    print("🚀 Inicializando banco de dados do Ministério do Meio Ambiente...")
    print("📊 Sistema de Monitoramento de Agrotóxicos Proibidos\n")
    
    create_tables()
    create_sample_users()
    
    print("\n🔒 Sistema pronto para uso!")
    print("🌐 Acesse: http://localhost:8000/docs para ver a API")
    print("🖥️  Frontend: http://localhost:3001")

if __name__ == "__main__":
    main()