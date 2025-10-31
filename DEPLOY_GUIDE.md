# Configurações de Produção para BioAccess
# 
# Para deploy em produção, você precisa configurar:

## 1. VARIÁVEIS DE AMBIENTE
# Crie um arquivo .env na raiz do backend com:

# Database (Supabase)
SUPABASE_DB_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase

# JWT Secret (gere uma chave segura)
JWT_SECRET=uma_chave_muito_segura_e_aleatoria_de_pelo_menos_32_caracteres

# Configurações do servidor
PORT=8001
HOST=0.0.0.0
ENVIRONMENT=production

# Configurações de CORS
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