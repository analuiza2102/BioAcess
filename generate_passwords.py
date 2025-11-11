#!/usr/bin/env python3
"""
Script para gerar hashes bcrypt de senhas
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definir senhas
passwords = {
    "usuario.teste": "teste123",
    "ministro.ambiente": "ministro2024",
    "analista.silva": "analista2024"
}

print("\n" + "="*80)
print("HASHES BCRYPT PARA INSERÇÃO NO BANCO DE DADOS")
print("="*80 + "\n")

for username, password in passwords.items():
    hash_pwd = pwd_context.hash(password)
    print(f"👤 Usuário: {username}")
    print(f"🔑 Senha: {password}")
    print(f"🔐 Hash: {hash_pwd}")
    print("-" * 80)

print("\n" + "="*80)
print("SQL COMPLETO PARA INSERIR OS USUÁRIOS")
print("="*80 + "\n")

print("-- Execute estes comandos no SQL Editor do Supabase:\n")

for username, password in passwords.items():
    hash_pwd = pwd_context.hash(password)
    
    if username == "usuario.teste":
        role = "public"
        clearance = 1
    elif username == "ministro.ambiente":
        role = "minister"
        clearance = 3
    else:  # analista.silva
        role = "director"
        clearance = 2
    
    print(f"""INSERT INTO users (username, password_hash, role, clearance, created_at)
VALUES (
  '{username}',
  '{hash_pwd}',
  '{role}',
  {clearance},
  NOW()
);
""")

print("\n" + "="*80)
print("✅ CREDENCIAIS DE ACESSO")
print("="*80 + "\n")

print("1. 👤 USUÁRIO TESTE (Clearance 1 - Público)")
print("   Username: usuario.teste")
print("   Senha: teste123")
print("   Acesso: Apenas dados públicos\n")

print("2. 🏛️ MINISTRO (Clearance 3 - Total)")
print("   Username: ministro.ambiente")
print("   Senha: ministro2024")
print("   Acesso: TODOS os dados e relatórios\n")

print("3. 📊 ANALISTA (Clearance 2 - Diretoria)")
print("   Username: analista.silva")
print("   Senha: analista2024")
print("   Acesso: Dados públicos + relatórios regionais\n")

print("="*80)
