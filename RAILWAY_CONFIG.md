# 🚀 Configurar Variáveis no Railway

## 📋 Acesse o Railway Dashboard

1. Vá em: https://railway.app/project/[seu-projeto]/service/bioaccess-api
2. Clique na aba **"Variables"**
3. Adicione cada variável abaixo:

---

## 🔑 Variáveis Obrigatórias

### 1. SUPABASE_DB_URL
```
postgresql://postgres:VmH7taAFTqgynxwj@db.krutpwnvwfynylefapeh.supabase.co:5432/postgres
```
**⚠️ IMPORTANTE:** Use a conexão **SEM pooler** (porta 5432, não 6543)

### 2. SUPABASE_URL
```
https://krutpwnvfynylefapeh.supabase.co
```

### 3. SUPABASE_KEY
Pegue em: Supabase → Settings → API → `anon` public key
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (sua key completa)
```

### 4. JWT_SECRET
Use o existente ou gere novo:
```bash
# No seu terminal local:
python -c "import secrets; print(secrets.token_urlsafe(64))"
```
Cole o resultado gerado. Exemplo:
```
OTQ1OTd1YW0tZDhqNC00TGYjMtMjNDNjMzQzZmZkMzI1NWFOGItZTM5Zi00YmJzdiOlMVViZjI1
```

### 5. CORS_ORIGINS
```
http://localhost:5173,https://bio-acess.vercel.app
```

### 6. PYTHON_VERSION
```
3.11.8
```

### 7. PYTHONUNBUFFERED
```
1
```

### 8. PORT
```
8000
```

---

## ✅ Como adicionar no Railway:

Para cada variável:
1. Clique em **"+ New Variable"**
2. Digite o **nome** (ex: `SUPABASE_DB_URL`)
3. Cole o **valor**
4. Clique em **"Add"**

---

## 🔄 Após adicionar todas:

O Railway vai fazer **redeploy automático**. Aguarde:
- ✅ Instalar dependências (3-4 min)
- ✅ Inicializar banco de dados
- ✅ Criar usuários demo
- ✅ Iniciar servidor

---

## 🧪 Testar após deploy:

### Health Check
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

### Login Demo
```bash
curl -X POST https://bioaccess-api-production.up.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'
```

---

## 🆘 Troubleshooting

### Erro: "relation 'users' does not exist"
- ✅ `start.py` cria as tabelas automaticamente
- Verifique logs no Railway: deve aparecer "Creating database tables..."

### Erro: "could not connect to server"
- ❌ Verifique se `SUPABASE_DB_URL` está correta
- ❌ Use porta **5432** (não 6543 pooler)
- ✅ Formato: `postgresql://postgres:SENHA@db.XXX.supabase.co:5432/postgres`

### Erro CORS
- ❌ Verifique `CORS_ORIGINS`
- ✅ Deve incluir: `https://bio-acess.vercel.app`
- ✅ Sem barra no final da URL

---

## 📝 Checklist Final

- [ ] 8 variáveis adicionadas no Railway
- [ ] Railway fez redeploy automático
- [ ] Health check retorna `{"status": "healthy"}`
- [ ] Login demo funciona
- [ ] Configurar `VITE_API_URL` no Vercel
- [ ] Testar frontend completo

🎉 Pronto! Seu backend estará rodando no Railway!
