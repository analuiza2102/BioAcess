# 🔑 Como Configurar SUPABASE_DB_URL no Render

## Passo 1: Pegar a URL de Conexão no Supabase

1. Acesse [Supabase Dashboard](https://supabase.com/dashboard)
2. Selecione seu projeto **BioAccess**
3. Vá em **Settings** (ícone ⚙️ no menu lateral)
4. Clique em **Database**
5. Role até **Connection String**
6. Copie a **URI** (não a connection pooling):

```
postgresql://postgres.krutpwnvwfynylefapeh:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

7. **IMPORTANTE:** Substitua `[YOUR-PASSWORD]` pela senha do banco
   - Se não lembra, pode resetar em **Database → Database Password → Reset**

---

## Passo 2: Configurar no Render

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Selecione o serviço **bioaccess-api**
3. Vá em **Environment** no menu lateral
4. Clique em **Add Environment Variable**
5. Adicione:

| Key | Value |
|-----|-------|
| `SUPABASE_DB_URL` | Cole a URL completa do Supabase aqui |

**Exemplo:**
```
postgresql://postgres.krutpwnvwfynylefapeh:SuaSenhaAqui@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

6. Clique em **Save Changes**

---

## Passo 3: Verificar se a URL está correta

A URL do Supabase deve seguir este formato:

```
postgresql://postgres.[PROJECT_REF]:[PASSWORD]@[HOST]:6543/postgres
```

Onde:
- `PROJECT_REF`: `krutpwnvwfynylefapeh` (do seu projeto)
- `PASSWORD`: senha do banco (sensível)
- `HOST`: geralmente `aws-0-us-east-1.pooler.supabase.com`

---

## ⚠️ Problemas Comuns

### "password authentication failed"
→ Senha incorreta. Resete a senha no Supabase:
1. **Settings → Database → Reset Database Password**
2. Copie a nova senha
3. Atualize `SUPABASE_DB_URL` no Render com a nova senha

### "could not connect to server"
→ Certifique-se de usar a **URI** (porta 6543), não a connection pooling.

### "SSL connection required"
→ Adicione `?sslmode=require` no final da URL:
```
postgresql://...postgres?sslmode=require
```

---

## ✅ Checklist Final

- [ ] URL copiada do Supabase (Settings → Database → Connection String)
- [ ] Senha substituída em `[YOUR-PASSWORD]`
- [ ] Variável `SUPABASE_DB_URL` adicionada no Render
- [ ] Deploy manual feito no Render
- [ ] Logs verificados: `✅ Conexão com banco OK`

---

**Seu schema já está criado no Supabase com as tabelas:**
- `users` ✅
- `audit_logs` ✅
- `biometric_templates` ✅

**Não precisa criar tabelas manualmente, o código usa o banco existente!**
