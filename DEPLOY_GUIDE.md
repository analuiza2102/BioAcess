# 🚀 Guia de Deploy - BioAccess

## Problemas Resolvidos

### ❌ Problemas Identificados:
1. **Render**: Erro `ModuleNotFoundError: No module named 'distutils'`
2. **Vercel**: Conflitos de configuração frontend/backend
3. **Dependências**: Versões incompatíveis do TensorFlow

### ✅ Soluções Implementadas:

## 📦 Deploy no Render (Backend)

### 1. Configurações do Render:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python render_start.py`
- **Environment**: Python 3.11
- **Region**: Oregon (US West)

### 2. Variáveis de Ambiente no Render:
FRONTEND_URL=https://seu-app.vercel.app

## 2. BANCO DE DADOS
# ✅ Você já está usando Supabase (PostgreSQL na nuvem)
# ✅ Não precisa de configuração adicional

## 3. OPÇÕES DE DEPLOY DO BACKEND

### OPÇÃO A: Railway (Recomendada - Mais Fácil)
# 1. Vá em: https://railway.app
# 2. Conecte seu GitHub
# 3. Deploy o backend automaticamente
# 4. Configure as variáveis de ambiente
# 5. Railway fornece URL automática

### OPÇÃO B: Render (Gratuita)
# 1. Vá em: https://render.com
# 2. Conecte seu GitHub
# 3. Crie um Web Service
# 4. Configure Python environment
# 5. Configure variáveis de ambiente

### OPÇÃO C: Heroku
# 1. Instale Heroku CLI
# 2. heroku create seu-app-backend
# 3. Configure variáveis de ambiente
# 4. git push heroku main

### OPÇÃO D: DigitalOcean App Platform
# 1. Conecte GitHub
# 2. Configure Python app
# 3. Configure variáveis de ambiente

## 4. CONFIGURAÇÕES NECESSÁRIAS

### Frontend (Vercel)
# Configure variável de ambiente:
VITE_API_BASE=https://sua-api-backend.railway.app

### Backend
# Configure CORS para permitir seu frontend:
FRONTEND_URL=https://seu-app.vercel.app