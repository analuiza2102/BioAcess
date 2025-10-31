#!/usr/bin/env python3
"""Script para verificar e corrigir dados do usuário ana.luiza"""

import os
import sys
from sqlalchemy import create_engine, text

# Configurar variáveis de ambiente
os.environ['SUPABASE_DB_URL'] = 'postgresql://postgres:qYfLVRxCw7LFMetP@db.krutpwnvwfynylefapeh.supabase.co:5432/postgres'

def main():
    try:
        # Conectar ao banco
        engine = create_engine(os.environ['SUPABASE_DB_URL'])
        
        print("🔍 Verificando dados do usuário ana.luiza...")
        
        with engine.connect() as conn:
            # Verificar dados atuais
            result = conn.execute(text("""
                SELECT id, username, role, clearance 
                FROM users 
                WHERE username = 'ana.luiza'
            """))
            
            user = result.fetchone()
            
            if user:
                print(f"✅ Usuário encontrado:")
                print(f"   ID: {user[0]}")
                print(f"   Username: {user[1]}")
                print(f"   Role: {user[2]}")
                print(f"   Clearance: {user[3]}")
                
                if user[2] == 'minister' and user[3] == 3:
                    print("✅ Dados estão corretos!")
                else:
                    print("⚠️ Corrigindo dados...")
                    conn.execute(text("""
                        UPDATE users 
                        SET role = 'minister', clearance = 3 
                        WHERE username = 'ana.luiza'
                    """))
                    conn.commit()
                    print("✅ Dados corrigidos!")
            else:
                print("❌ Usuário ana.luiza não encontrado!")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)