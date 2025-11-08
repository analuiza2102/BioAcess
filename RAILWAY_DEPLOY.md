# 🚂 Deploy BioAccess no Railway.app

## 🎯 Por Que Railway?

- ✅ **$5 de crédito grátis/mês** (suficiente para uso moderado)
- ✅ **Até 8GB RAM** disponível
- ✅ **Deploy automático** via GitHub
- ✅ **Mais rápido** que Render
- ✅ **Suporta TensorFlow** perfeitamente

## 📋 Variáveis de Ambiente Necessárias

### 1. Database (Supabase PostgreSQL)
```
SUPABASE_DB_URL=postgresql://postgres.krutpwnvfynylefapeh:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```
**Onde encontrar**: 
- Acesse seu projeto no Supabase
- Settings → Database → Connection String
- Use a Connection Pooling (porta 6543)

### 2. Supabase API
```
SUPABASE_URL=https://krutpwnvfynylefapeh.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
**Onde encontrar**:
- Supabase → Settings → API
- SUPABASE_URL: URL da API
- SUPABASE_KEY: anon/public key

### 3. JWT Secret (Segurança)
```
JWT_SECRET=OTQ1OTd1YW0tZDhqNC00TGYjMtMjNDNjMzQzZmZkMzI1NWFOGItZTM5Zi00YmJzdiOlMVViZjI1
```
**Pode usar o existente ou gerar novo**:
```powershell
# Gerar novo JWT_SECRET
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

### 4. CORS (Permitir requisições do frontend)
```
CORS_ORIGINS=http://localhost:5173,https://bio-acess.vercel.app
```
**Adicione sua URL do Vercel**

### 5. Python (Versão)
```
PYTHON_VERSION=3.11.8
```

### 6. Reconhecimento Facial (Opcional)
```
FACIAL_RECOGNITION_SERVICE_URL=
```
**Deixe vazio** - o Railway rodará o reconhecimento localmente

### 7. Outras configurações
```
PYTHONUNBUFFERED=1
PORT=8000
```

## 📦 Resumo - Copie e Cole no Railway

```env
# Database
SUPABASE_DB_URL=postgresql://postgres.krutpwnvfynylefapeh:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres

# Supabase API
SUPABASE_URL=https://krutpwnvfynylefapeh.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtydXRwd252ZnlueWxlZmFwZWgiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTczMDgyNTU4MCwiZXhwIjoyMDQ2NDAxNTgwfQ.dTcAVNtc4NQWzoMVNWjMjNDNjMzQzZmZkMzI1NWFOGItZTM5Zi00YmJzdiOlMVViZjI1

# Security
JWT_SECRET=OTQ1OTd1YW0tZDhqNC00TGYjMtMjNDNjMzQzZmZkMzI1NWFOGItZTM5Zi00YmJzdiOlMVViZjI1

# CORS
CORS_ORIGINS=http://localhost:5173,https://bio-acess.vercel.app

# Python
PYTHON_VERSION=3.11.8
PYTHONUNBUFFERED=1
PORT=8000

# Facial Recognition (deixe vazio para usar local)
FACIAL_RECOGNITION_SERVICE_URL=
```

## 🚀 Passo a Passo - Deploy no Railway

### 1. Criar Conta no Railway
1. Acesse: https://railway.app
2. Clique em **"Start a New Project"**
3. Login com GitHub

### 2. Conectar Repositório
1. Clique em **"Deploy from GitHub repo"**
2. Selecione **"analuiza2102/BioAcess"**
3. Railway detectará automaticamente as configurações

### 3. Configurar Variáveis de Ambiente
1. Clique no seu projeto
2. Vá em **"Variables"** (ícone de engrenagem)
3. Clique em **"+ New Variable"**
4. Cole **todas as variáveis** acima (uma por linha)
5. Ou importe de arquivo:
   - Clique em **"RAW Editor"**
   - Cole todo o bloco de variáveis
   - Clique em **"Save"**

### 4. Deploy Automático
1. Railway iniciará o deploy automaticamente
2. Acompanhe em **"Deployments"**
3. Aguarde 10-15 minutos (TensorFlow demora)
4. Status mudará para **"Active"** quando pronto

### 5. Obter URL Pública
1. Vá em **"Settings"**
2. Seção **"Networking"**
3. Clique em **"Generate Domain"**
4. Copie a URL: `https://bioaccess-production.up.railway.app`

### 6. Atualizar Frontend (Vercel)
Atualize a URL da API no Vercel:
```env
VITE_API_URL=https://bioaccess-production.up.railway.app
```

## 🔍 Verificação e Testes

### 1. Testar Health Check
```powershell
# Substitua pela sua URL
curl https://bioaccess-production.up.railway.app/health
```

**Resposta esperada**:
```json
{"status": "healthy"}
```

### 2. Testar Login Tradicional
```powershell
curl -X POST https://bioaccess-production.up.railway.app/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"username":"ana.luiza","password":"senha123"}'
```

### 3. Verificar Logs
No Railway:
1. Clique em **"Deployments"**
2. Selecione o deploy ativo
3. Veja os logs em tempo real
4. Procure por: `✅ DeepFace carregado com sucesso`

## 💰 Monitoramento de Créditos

Railway oferece **$5 grátis/mês**:

### Uso Estimado:
- **Servidor ativo 24/7**: ~$5-7/mês
- **Apenas em uso (com sleep)**: ~$2-3/mês

### Ver Uso Atual:
1. Railway Dashboard
2. Clique no ícone do usuário (canto superior direito)
3. **"Account Settings"** → **"Usage"**

### Dica para Economizar:
Configure sleep quando inativo:
1. **Settings** → **"Deploy Triggers"**
2. Ative **"Sleep after 15 minutes of inactivity"**
3. Reduz custo para ~$2/mês

## 🐛 Troubleshooting

### Deploy Falha
**Erro**: "Out of memory"
**Solução**: Aumentar RAM nas Settings → Resources

### TensorFlow Não Carrega
**Erro**: "No module named 'tensorflow'"
**Solução**: Verificar logs do build, redeployar

### Conexão com Supabase Falha
**Erro**: "Connection refused"
**Solução**: Verificar SUPABASE_DB_URL (usar Connection Pooling porta 6543)

### CORS Error no Frontend
**Solução**: Adicionar URL do Vercel em `CORS_ORIGINS`

## 📊 Comparação Final

| Item | Render Standard | Railway |
|------|----------------|---------|
| **Custo** | $7/mês | $5/mês (crédito) |
| **RAM** | 2GB | Até 8GB |
| **Deploy** | 15-20 min | 10-15 min |
| **Interface** | Simples | Muito simples |
| **Performance** | Boa | Excelente |
| **Recomendação** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## ✅ Checklist Final

- [ ] Conta criada no Railway
- [ ] Repositório conectado
- [ ] Todas variáveis de ambiente configuradas
- [ ] Deploy completado com sucesso
- [ ] URL pública gerada
- [ ] Health check funcionando
- [ ] Frontend atualizado com nova URL
- [ ] Login tradicional testado
- [ ] Reconhecimento facial testado

## 🎯 Após Deploy

1. **Commit das mudanças** (railway.json, nixpacks.toml):
```powershell
git add railway.json nixpacks.toml RAILWAY_DEPLOY.md
git commit -m "feat: adicionar configurações para deploy no Railway"
git push origin main
```

2. **Atualizar URL no Frontend** (Vercel):
   - Settings → Environment Variables
   - Atualizar `VITE_API_URL`

3. **Testar aplicação completa**:
   - Login tradicional
   - Login por câmera
   - Dashboard
   - Relatórios

---

**Status**: ✅ Pronto para deploy no Railway  
**Custo**: $5/mês (crédito grátis)  
**Tempo**: ~15 minutos  
**Data**: 8 de novembro de 2025
