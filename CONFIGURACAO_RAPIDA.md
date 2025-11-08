# 🚀 Configuração Rápida - BioAccess

## ✅ URL da API Railway
```
https://bioaccess-api-production.up.railway.app
```

## 📋 Checklist de Deploy

### 1. Backend (Railway) ✅
- [x] Código enviado para GitHub
- [x] Projeto conectado no Railway
- [x] Variáveis de ambiente configuradas
- [x] Deploy realizado com sucesso
- [x] URL gerada: `bioaccess-api-production.up.railway.app`

### 2. Frontend (Vercel) ⏳

#### Passo 1: Configurar variável no Vercel
1. Acesse: https://vercel.com/analuiza2102/bio-acess/settings/environment-variables
2. Adicione:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://bioaccess-api-production.up.railway.app`
   - **Environment**: Production, Preview, Development (selecionar todos)
3. Clique em "Save"

#### Passo 2: Redeploy
1. Vá em: https://vercel.com/analuiza2102/bio-acess/deployments
2. Clique nos "..." do último deploy
3. Clique em "Redeploy"
4. Aguarde 1-2 minutos

### 3. Teste Final 🧪

#### Health Check (API)
```bash
curl https://bioaccess-api-production.up.railway.app/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-08T..."
}
```

#### Login Tradicional
```bash
curl -X POST https://bioaccess-api-production.up.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'
```

#### Testar Frontend
1. Acesse: https://bio-acess.vercel.app
2. Faça login com:
   - **Usuário**: demo
   - **Senha**: demo123
3. Teste o reconhecimento facial

## 🔧 Desenvolvimento Local

### Backend
```bash
cd src/backend
python -m venv venv
venv\Scripts\activate
pip install -r ../../requirements.txt
python run_server.py
```

### Frontend
```bash
npm install
npm run dev
```

O arquivo `.env.local` já está configurado com a URL do Railway.

## 📝 Variáveis de Ambiente

### Railway (Backend)
✅ Todas configuradas:
- `SUPABASE_DB_URL`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `JWT_SECRET`
- `CORS_ORIGINS`
- `PYTHON_VERSION`
- `PYTHONUNBUFFERED`
- `PORT`

### Vercel (Frontend)
⏳ Falta adicionar:
- `VITE_API_URL=https://bioaccess-api-production.up.railway.app`

## 🎯 Próximos Passos

1. **Commitar mudanças**:
```bash
git add .
git commit -m "Configuração final: Railway API URL e limpeza Render"
git push origin main
```

2. **Configurar VITE_API_URL no Vercel** (ver Passo 1 acima)

3. **Redeploy no Vercel** (ver Passo 2 acima)

4. **Testar aplicação completa** 🎉

## 🆘 Troubleshooting

### CORS Error
Se aparecer erro de CORS, verifique no Railway:
- `CORS_ORIGINS` deve incluir: `https://bio-acess.vercel.app`

### API não responde
1. Verifique logs no Railway Dashboard
2. Confirme que todas as variáveis estão configuradas
3. Verifique se o build foi concluído

### Reconhecimento facial não funciona
1. Confirme que `VITE_API_URL` está configurada no Vercel
2. Verifique no console do navegador se a URL está correta
3. Teste o endpoint `/auth/verify-biometric` diretamente

## 💰 Custos Mensais
- **Railway**: ~$5/mês (8GB RAM)
- **Vercel**: Grátis (Hobby plan)
- **Supabase**: Grátis (até 500MB)

**Total**: ~$5/mês 💰
