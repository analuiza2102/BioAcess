# ⚡ AÇÃO RÁPIDA - Deploy Corrigido

## 🎯 O Que Você Precisa Fazer AGORA

### 1️⃣ Commit e Push (você já fez `git add .`)

```bash
git commit -m "fix: configurar conexão Supabase e corrigir CORS"
git push origin main
```

### 2️⃣ Pegar URL do Supabase

1. Acesse https://supabase.com/dashboard
2. Selecione seu projeto
3. **Settings → Database → Connection String → URI**
4. Copie algo como:
   ```
   postgresql://postgres.krutpwnvwfynylefapeh:[SUA-SENHA]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
5. **Substitua `[SUA-SENHA]`** pela senha real do banco

### 3️⃣ Configurar no Render

1. Acesse https://dashboard.render.com
2. Selecione **bioaccess-api**
3. **Environment → Add Environment Variable**
4. Adicione:

```
SUPABASE_DB_URL = postgresql://postgres.krutpwnvwfynylefapeh:SUA_SENHA_AQUI@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

5. Também adicione/atualize:

```
CORS_ORIGINS = http://localhost:5173,https://bio-acess.vercel.app,https://bio-acess-o7ra1en0k-ana-luiza-guimaraes-luizaos-projects.vercel.app
```

6. **Save Changes**

### 4️⃣ Redeploy Manual

1. No Render: **Manual Deploy → Deploy latest commit**
2. Aguarde 2-3 minutos

### 5️⃣ Verificar Logs

Procure por:
```
✅ Conexão com banco OK - X usuários existentes
🌐 CORS Origins configuradas: [...]
```

---

## ✅ O Que Foi Corrigido

| Problema | Solução |
|----------|---------|
| ❌ `no such table: users` | Configurar `SUPABASE_DB_URL` corretamente |
| ❌ CORS bloqueando | Corrigir formato das origens |
| ❌ Erro 500 sem detalhes | Handler de exceções adicionado |

---

## 📁 Arquivos Criados

- **`SUPABASE_SETUP.md`** - Guia detalhado do Supabase
- **`CORRECOES_RENDER.md`** - Documentação completa
- **`test_render_deploy.ps1`** - Script de teste

---

## 🧪 Teste Final (após deploy)

```powershell
.\test_render_deploy.ps1
```

---

**Dúvidas? Me chame! 🚀**
