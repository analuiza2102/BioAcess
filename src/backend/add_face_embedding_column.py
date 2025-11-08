"""
Script para adicionar coluna face_embedding na tabela users
Execute: python src/backend/add_face_embedding_column.py
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('.env.local')

DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('SUPABASE_DB_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrada")
    exit(1)

print(f"🔗 Conectando ao banco: {DATABASE_URL[:30]}...")

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Verificar se a coluna já existe
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='face_embedding'
        """))
        
        if result.fetchone():
            print("✅ Coluna face_embedding já existe!")
        else:
            # Adicionar coluna
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN face_embedding TEXT NULL
            """))
            conn.commit()
            print("✅ Coluna face_embedding adicionada com sucesso!")
            
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
