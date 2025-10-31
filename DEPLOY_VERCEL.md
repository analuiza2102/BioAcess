# 🚀 Deploy Frontend BioAccess no Vercel - Guia Completo

## 📋 **Pré-requisitos:**
- ✅ Backend já deployado no Render (em andamento)
- ✅ Repositório GitHub atualizado
- ✅ Conta no Vercel (vercel.com)

## 🎯 **Passos para Deploy no Vercel:**

### 1. **Preparação Final do Frontend:**
```powershell
# Verificar se o build funciona localmente
cd "c:\Users\Ana Luiza\Desktop\Bioaccess Setup"
npm run build

# Se der erro, instalar dependências
npm install --legacy-peer-deps
npm run build
```

### 2. **Acessar o Vercel Dashboard:**
- Acesse: https://vercel.com/dashboard
- Faça login com GitHub (recomendado)

### 3. **Criar Novo Projeto:**
- **Clique em "New Project"**
- **Conecte o repositório GitHub:** `analuiza2102/BioAcess`
- **Selecione o repositório** BioAcess

### 4. **Configurações do Deploy:**
```yaml
# Configurações que aparecerão automaticamente:
Project Name: bioaccess-frontend
Framework: Vite
Root Directory: ./
Build Command: npm run build  
Output Directory: dist
Install Command: npm install
```

### 5. **Variáveis de Ambiente (IMPORTANTE):**
Adicione no painel do Vercel:
```env
# Backend URL (aguardar URL do Render)
VITE_API_URL=https://seu-backend.onrender.com

# Se necessário para desenvolvimento
NODE_ENV=production
```

### 6. **Deploy:**
- **Clique em "Deploy"**
- Aguardar build (2-5 minutos)
- ✅ Sucesso!

## 🔗 **Conectar Frontend ao Backend:**

### Após Render Deploy Completo:
1. **Copiar URL do backend Render:**
   - Ex: `https://bioaccess-api.onrender.com`

2. **Atualizar variável no Vercel:**
   - Dashboard > Projeto > Settings > Environment Variables
   - `VITE_API_URL` = URL do backend Render

3. **Redeploy no Vercel:**
   - Dashboard > Deployments > "Redeploy"

## 📁 **Estrutura de Deploy:**
```
Arquitetura Final:
├── 🌐 Frontend (Vercel)
│   ├── React + TypeScript + Vite
│   ├── URL: https://bioaccess-frontend.vercel.app
│   └── Conecta com backend via VITE_API_URL
│
├── 🔧 Backend API (Render)  
│   ├── FastAPI + Python
│   ├── URL: https://bioaccess-api.onrender.com
│   └── Banco: Supabase PostgreSQL
│
└── 💾 Database (Supabase)
    └── PostgreSQL gerenciado
```

## ⚡ **Configurações Avançadas (Opcional):**

### Custom Domain:
- Dashboard > Project > Settings > Domains
- Adicionar domínio customizado

### Performance:
- Edge Functions: Habilitadas automaticamente
- CDN Global: Ativo por padrão
- Compressão: Automática

## 🔍 **Troubleshooting:**

### Se build falhar:
```bash
# Build local para testar
npm run build

# Verificar dependências
npm install --legacy-peer-deps
```

### Se API não conectar:
1. Verificar VITE_API_URL no Vercel
2. Confirmar URL do backend Render
3. Verificar CORS no backend

## 📊 **Monitoramento:**
- **Logs:** Vercel Dashboard > Functions > View Function Logs
- **Analytics:** Dashboard > Analytics  
- **Performance:** Automatically tracked

## 🎯 **Status Atual:**
- ✅ vercel.json configurado
- ✅ package.json otimizado  
- ✅ Build local funcionando
- ⏳ Aguardando URL do backend Render

## 🚀 **Próximo Passo:**
**Acesse https://vercel.com/dashboard e siga o guia acima!**

---

### ⚠️ **Importante:**
1. **Aguarde o backend Render finalizar** para ter a URL correta
2. **Configure CORS no backend** para aceitar domínio do Vercel  
3. **Teste todas as funcionalidades** após deploy completo