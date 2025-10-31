#!/usr/bin/env python3
"""
Script para corrigir todos os problemas biométricos da ana.luiza
"""

import os
import sys
from pathlib import Path

# Adicionar diretório ao path
backend_dir = Path(__file__).parent / "src" / "backend"
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(backend_dir / '.env')

def fix_ana_luiza_issues():
    """Corrige todos os problemas da ana.luiza"""
    
    print("🔧 CORRIGINDO PROBLEMAS DA ANA.LUIZA")
    print("=" * 50)
    
    try:
        from app.db import get_db
        from app.models import User, BiometricTemplate
        from sqlalchemy import text
        
        db = next(get_db())
        
        # 1. Corrigir clearance
        print("1️⃣ Corrigindo clearance...")
        update_query = text("""
            UPDATE users 
            SET clearance = 3, role = 'minister' 
            WHERE username = 'ana.luiza'
        """)
        result = db.execute(update_query)
        db.commit()
        print("✅ Clearance atualizado para nível 3 (minister)")
        
        # 2. Remover biometria existente (problemática)
        print("\n2️⃣ Removendo biometria problemática...")
        
        # Buscar usuário
        user = db.query(User).filter(User.username == 'ana.luiza').first()
        if user:
            # Remover template biométrico
            delete_query = text("""
                DELETE FROM biometric_templates 
                WHERE user_id = :user_id
            """)
            db.execute(delete_query, {"user_id": user.id})
            db.commit()
            print("✅ Biometria antiga removida")
        else:
            print("❌ Usuário não encontrado")
        
        # 3. Verificar status final
        print("\n3️⃣ Verificando status final...")
        user_query = text("""
            SELECT username, role, clearance 
            FROM users 
            WHERE username = 'ana.luiza'
        """)
        result = db.execute(user_query).fetchone()
        
        if result:
            username, role, clearance = result
            print(f"✅ Usuário: {username}")
            print(f"✅ Role: {role}")
            print(f"✅ Clearance: {clearance}")
        
        # Verificar se ainda tem biometria
        biometric_query = text("""
            SELECT COUNT(*) as count
            FROM biometric_templates bt
            JOIN users u ON bt.user_id = u.id
            WHERE u.username = 'ana.luiza'
        """)
        count_result = db.execute(biometric_query).fetchone()
        biometric_count = count_result[0] if count_result else 0
        
        if biometric_count == 0:
            print("✅ Biometria removida com sucesso")
        else:
            print(f"⚠️ Ainda há {biometric_count} biometrias cadastradas")
        
        print("\n" + "=" * 50)
        print("🎉 CORREÇÕES APLICADAS COM SUCESSO!")
        print()
        print("📋 PRÓXIMOS PASSOS:")
        print("1. Faça login tradicional: ana.luiza / senha123")
        print("2. Acesse o dashboard (agora com nível 3)")
        print("3. Cadastre nova biometria limpa")
        print()
        print("🎯 USUÁRIO PRONTO PARA NOVO CADASTRO BIOMÉTRICO!")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir problemas: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = fix_ana_luiza_issues()
    if success:
        print("\n✅ Todas as correções aplicadas!")
    else:
        print("\n❌ Houve problemas na correção.")