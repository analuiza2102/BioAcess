"""
🔧 Script para criar usuários no Supabase com senhas compatíveis com bcrypt
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import engine, Base, SessionLocal
from app.models import User
from passlib.context import CryptContext

# Configuração do bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_users():
    print("🚀 Criando usuários no Supabase...")
    print("📊 Sistema de Monitoramento de Agrotóxicos Proibidos\n")
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas no Supabase")
    
    # Usuários com senhas simples (compatível com bcrypt)
    sample_users = [
        {
            "username": "ana.luiza",
            "password": "senha123",  # 9 chars - OK
            "role": "public",
            "clearance": 1,
            "description": "Acesso público - funcionária padrão"
        },
        {
            "username": "diretor.silva",
            "password": "diretor24",  # 9 chars - OK
            "role": "director", 
            "clearance": 2,
            "description": "Diretor de Divisão - relatórios regionais"
        },
        {
            "username": "ministro.ambiente",
            "password": "ministro24",  # 10 chars - OK
            "role": "minister",
            "clearance": 3,
            "description": "Ministro do Meio Ambiente - acesso total"
        },
        {
            "username": "fiscal.gomes",
            "password": "fiscal123",  # 10 chars - OK
            "role": "director",
            "clearance": 2, 
            "description": "Fiscal ambiental - monitoramento regional"
        },
        {
            "username": "analista.santos",
            "password": "analista1",  # 9 chars - OK
            "role": "public",
            "clearance": 1,
            "description": "Analista ambiental - dados públicos"
        }
    ]
    
    db = SessionLocal()
    
    try:
        for user_data in sample_users:
            # Verifica se usuário já existe
            existing = db.query(User).filter(User.username == user_data["username"]).first()
            if existing:
                print(f"⚠️  Usuário {user_data['username']} já existe, pulando...")
                continue
            
            # Hash da senha (versão simplificada)
            password = user_data["password"]
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
            
            print(f"✅ Criado: {user_data['username']} (clearance {user_data['clearance']}) - {user_data['description']}")
        
        print("\n🎉 Usuários criados no Supabase com sucesso!")
        print("\n📝 CREDENCIAIS PARA TESTE:")
        print("┌─────────────────────┬──────────────┬───────────┬─────────────────────────────────┐")
        print("│ Usuário             │ Senha        │ Clearance │ Descrição                       │")
        print("├─────────────────────┼──────────────┼───────────┼─────────────────────────────────┤")
        for user_data in sample_users:
            print(f"│ {user_data['username']:<19} │ {user_data['password']:<12} │ Nível {user_data['clearance']}   │ {user_data['description']:<31} │")
        print("└─────────────────────┴──────────────┴───────────┴─────────────────────────────────┘")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuários: {e}")
    finally:
        db.close()
    
    print("\n🔒 Sistema pronto para uso!")
    print("🌐 Supabase: https://krutpwnvwfynylefapeh.supabase.co")
    print("🖥️  API: http://localhost:8000/docs")
    print("🌐 Frontend: http://localhost:3003")

if __name__ == "__main__":
    create_users()