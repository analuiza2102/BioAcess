"""
Script para limpar usuários desnecessários do banco de dados
Mantém apenas 3 usuários essenciais:
- ana.luiza (Ministro - Nível 3)
- diretor.silva (Diretor - Nível 2)  
- funcionario.costa (Público - Nível 1)
"""

import os
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.biometric_template import BiometricTemplate

# Configurar conexão com o banco
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL não configurada!")
    exit(1)

print(f"🔗 Conectando ao banco...")
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
db = Session()

try:
    # Usuários que devem ser mantidos
    usuarios_manter = ["ana.luiza", "diretor.silva", "funcionario.costa"]
    
    print(f"📋 Buscando usuários no banco...")
    todos_usuarios = db.execute(select(User)).scalars().all()
    print(f"✅ Total de usuários: {len(todos_usuarios)}")
    
    for user in todos_usuarios:
        print(f"  - {user.username} ({user.role}, clearance={user.clearance})")
    
    # Identificar usuários para deletar
    usuarios_deletar = [u for u in todos_usuarios if u.username not in usuarios_manter]
    
    if not usuarios_deletar:
        print(f"\n✅ Banco já está limpo! Apenas os 3 usuários essenciais estão presentes.")
    else:
        print(f"\n🗑️  Deletando {len(usuarios_deletar)} usuários...")
        
        for user in usuarios_deletar:
            # Deletar biometrias associadas primeiro
            biometrias = db.execute(
                select(BiometricTemplate).where(BiometricTemplate.user_id == user.id)
            ).scalars().all()
            
            for bio in biometrias:
                db.delete(bio)
                print(f"  ❌ Biometria deletada para: {user.username}")
            
            # Deletar usuário
            db.delete(user)
            print(f"  ❌ Usuário deletado: {user.username}")
        
        db.commit()
        print(f"\n✅ Limpeza concluída!")
    
    # Verificar se funcionario.costa existe, senão criar
    funcionario = db.execute(select(User).where(User.username == "funcionario.costa")).scalar_one_or_none()
    
    if not funcionario:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        print(f"\n👤 Criando usuário 'funcionario.costa'...")
        novo_usuario = User(
            username="funcionario.costa",
            password_hash=pwd_context.hash("funcionario123"),
            role="public",
            clearance=1
        )
        db.add(novo_usuario)
        db.commit()
        print(f"✅ Usuário 'funcionario.costa' criado!")
    
    # Mostrar usuários finais
    print(f"\n📋 Usuários finais no banco:")
    usuarios_finais = db.execute(select(User)).scalars().all()
    for user in usuarios_finais:
        print(f"  ✓ {user.username} - {user.role} (Nível {user.clearance})")

except Exception as e:
    print(f"❌ Erro: {e}")
    db.rollback()
finally:
    db.close()
    print(f"\n🔒 Conexão fechada.")
