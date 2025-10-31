#!/usr/bin/env python3
"""
Script de verificação de dependências para o Render
Executa antes do deploy para garantir compatibilidade
"""

import sys
import subprocess
import importlib

def test_import(package_name, import_as=None):
    """Testa importação de um pacote"""
    try:
        if import_as:
            importlib.import_module(import_as)
        else:
            importlib.import_module(package_name)
        print(f"✅ {package_name}: OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: ERRO - {e}")
        return False

def main():
    print("🔍 Verificando dependências para Render.com...\n")
    
    # Lista de dependências críticas
    dependencies = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("sqlalchemy", "sqlalchemy"),
        ("supabase", "supabase"),
        ("deepface", "deepface"),
        ("tensorflow", "tensorflow"),
        ("opencv-python-headless", "cv2"),
        ("numpy", "numpy"),
        ("pillow", "PIL"),
        ("python-jose", "jose"),
        ("passlib", "passlib"),
        ("pydantic", "pydantic"),
        ("python-dotenv", "dotenv")
    ]
    
    failed = []
    for package, import_name in dependencies:
        if not test_import(package, import_name):
            failed.append(package)
    
    print(f"\n📊 Resultado:")
    print(f"✅ Sucessos: {len(dependencies) - len(failed)}")
    print(f"❌ Falhas: {len(failed)}")
    
    if failed:
        print(f"\n🚨 Pacotes com problema:")
        for package in failed:
            print(f"  - {package}")
        sys.exit(1)
    else:
        print(f"\n🎉 Todas as dependências estão OK para o Render!")
        
        # Teste básico do DeepFace
        try:
            from deepface import DeepFace
            print("🔬 Testando DeepFace...")
            # Não executar análise real, apenas verificar se carrega
            print("✅ DeepFace pronto para uso")
        except Exception as e:
            print(f"⚠️ DeepFace warning: {e}")
    
if __name__ == "__main__":
    main()