# 🚂 RAILWAY - RESUMO RÁPIDO

## 📋 VARIÁVEIS DE AMBIENTE - Copie e Cole no Railway

```env
SUPABASE_DB_URL=postgresql://postgres.krutpwnvfynylefapeh:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://krutpwnvfynylefapeh.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtydXRwd252ZnlueWxlZmFwZWgiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTczMDgyNTU4MCwiZXhwIjoyMDQ2NDAxNTgwfQ.dTcAVNtc4NQWzoMVNWjMjNDNjMzQzZmZkMzI1NWFOGItZTM5Zi00YmJzdiOlMVViZjI1
JWT_SECRET=OTQ1OTd1YW0tZDhqNC00TGYjMtMjNDNjMzQzZmZkMzI1NWFOGItZTM5Zi00YmJzdiOlMVViZjI1
CORS_ORIGINS=http://localhost:5173,https://bio-acess.vercel.app
PYTHON_VERSION=3.11.8
PYTHONUNBUFFERED=1
PORT=8000
```

## 🚀 PASSO A PASSO

### 1️⃣ Acessar Railway
- Site: https://railway.app
- Login com GitHub

### 2️⃣ Criar Projeto
- "Deploy from GitHub repo"
- Selecionar: analuiza2102/BioAcess

### 3️⃣ Configurar Variáveis
- Clicar em "Variables"
- "RAW Editor"
- Colar TODAS as variáveis acima
- "Save"

### 4️⃣ Deploy Automático
- Railway faz deploy sozinho
- Aguardar 10-15 minutos
- Status: "Active" quando pronto

### 5️⃣ Gerar URL
- Settings → Networking
- "Generate Domain"
- Copiar URL gerada

### 6️⃣ Atualizar Frontend
- Vercel → Settings → Environment Variables
- VITE_API_URL = URL do Railway

## ✅ TESTAR

```powershell
# Health check
curl https://SUA-URL.railway.app/health

# Login
curl -X POST https://SUA-URL.railway.app/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"username":"ana.luiza","password":"senha123"}'
```

## 💰 CUSTO

- $5/mês (crédito grátis)
- Suficiente para uso moderado
- Configure "Sleep" para economizar

## 🔧 AJUDA

Problemas? Veja: RAILWAY_DEPLOY.md (guia completo)
