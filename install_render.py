#!/usr/bin/env python3
"""
Script de build personalizado para Render.com
Resolve problemas de dependências do TensorFlow
"""

import subprocess
import sys
import os

def install_package(package, description=""):
    """Instala um pacote específico com tratamento de erros"""
    print(f"📦 Instalando {description or package}...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package, 
            "--no-cache-dir", "--force-reinstall"
        ], check=True, capture_output=True, text=True)
        print(f"✅ {package} instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {package}: {e.stderr}")
        return False

def main():
    print("🚀 Iniciando instalação customizada para Render.com...")
    
    # Atualizar pip primeiro
    print("📥 Atualizando pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    # Instalar dependências críticas primeiro
    critical_deps = [
        ("setuptools==69.5.1", "Build tools"),
        ("wheel==0.42.0", "Wheel support"),
        ("numpy==1.24.3", "NumPy"),
        ("tensorflow-cpu==2.15.0", "TensorFlow CPU"),
    ]
    
    for package, desc in critical_deps:
        if not install_package(package, desc):
            print(f"🚨 Falha crítica ao instalar {package}")
            sys.exit(1)
    
    # Instalar o resto via requirements
    print("📋 Instalando requirements restantes...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements_render.txt",
            "--no-cache-dir"
        ], check=True)
        print("✅ Todas as dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação final: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()