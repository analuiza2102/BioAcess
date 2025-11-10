# 🚀 CONFIGURAR RAILWAY AGORA

## 📋 Copie esta Connection String:

**OPÇÃO 1 - Connection Pooling (Recomendado para Railway):**
```
postgresql://postgres.krutpwnvwfynylefapeh:qYfLVRxCw7LFMetP@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**OPÇÃO 2 - Conexão Direta (se a primeira não funcionar):**
```
postgresql://postgres:qYfLVRxCw7LFMetP@db.krutpwnvwfynylefapeh.supabase.co:5432/postgres
```

## ⚙️ Passos no Railway:

1. **Acesse**: https://railway.app → Seu projeto → **bioaccess-api**

2. **Clique em**: `Variables` (aba superior)

3. **Adicione ou edite** a variável:
   ```
   Name:  SUPABASE_DB_URL
   Value: postgresql://postgres:qYfLVRxCw7LFMetP@db.krutpwnvwfynylefapeh.supabase.co:5432/postgres
   ```

4. **Clique em** `Add` ou `Save`

5. **Aguarde**: Railway vai fazer redeploy automaticamente (1-2 min)

## ✅ Verificar se funcionou:

Depois do redeploy, vá em **Deployments** → **View Logs** e procure por:

```
✅ Conexão OK - X usuários
✅ Banco inicializado!
🌟 Starting uvicorn server...
```

Se aparecer isso, **SUCESSO!** ✅

## 🔗 Próximo Passo: Configurar Vercel

Depois que o Railway estiver OK, adicione no Vercel:

```
VITE_API_URL = https://bioaccess-api-production.up.railway.app
```

E faça redeploy do Vercel.

---

**Seu sistema estará 100% funcional! 🎉**
