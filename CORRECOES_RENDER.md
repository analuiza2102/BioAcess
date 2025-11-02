# Correções Aplicadas - Render.com Deploy

## 🔧 Problemas Identificados e Corrigidos

### 1. **Erro: `sqlite3.OperationalError: no such table: users`**

**Causa:** O banco de dados não estava sendo inicializado corretamente devido a:
- `SUPABASE_DB_URL` obrigatório mas não fornecido
- Erro silencioso no `render_start.py` que continuava mesmo com falha

**Correção:**
- ✅ Tornamos `SUPABASE_DB_URL` opcional em `config.py`
- ✅ Adicionamos `DATABASE_URL` como alias
- ✅ Melhoramos logging e tratamento de erros no `render_start.py`
- ✅ Script agora **para completamente** se o banco falhar (antes continuava)

### 2. **CORS Bloqueando Preflight (OPTIONS)**

**Causa:** Formato JSON incorreto no `render.yaml`:
```yaml
# ❌ ERRADO
CORS_ORIGINS: '["http://localhost:5173","..."]'
```

**Correção:**
```yaml
# ✅ CORRETO
CORS_ORIGINS: http://localhost:5173,http://localhost:3000,https://bio-acess.vercel.app
```

### 3. **Exception Handler Global**

Adicionamos handler em `main.py` para capturar e logar **todos** os erros 500:
```python
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.method} {request.url}: {exc}")
    return JSONResponse(status_code=500, ...)
```

---

## 📋 Checklist de Deploy no Render

### Passo 1: Commit e Push
```bash
git add .
git commit -m "fix: corrigir CORS e inicialização do banco no Render"
git push origin main
```

### Passo 2: Configurar Variáveis de Ambiente no Render

Acesse **Render Dashboard → bioaccess-api → Environment**:

1. **SUPABASE_DB_URL** (OBRIGATÓRIO - URL de conexão do Supabase):
   ```
   postgresql://postgres:[SUA-SENHA]@db.krutpwnvwfynylefapeh.supabase.co:5432/postgres
   ```
   > ⚠️ **IMPORTANTE:** Pegue essa URL em **Supabase → Project Settings → Database → Connection String (URI)**
   > Substitua `[YOUR-PASSWORD]` pela senha do banco

2. **CORS_ORIGINS** (substitua pela lista completa):
   ```
   http://localhost:5173,http://localhost:3000,https://bio-acess.vercel.app,https://bio-acess-o7ra1en0k-ana-luiza-guimaraes-luizaos-projects.vercel.app
   ```

3. **JWT_SECRET** (gere um novo ou use o auto-generated do Render):
   ```
   [deixe o Render gerar automaticamente ou cole um valor seguro]
   ```

4. **Remova DATABASE_URL** se existir (vamos usar só SUPABASE_DB_URL para evitar conflito)

### Passo 3: Redeploy Manual

1. Vá em **Manual Deploy → Deploy latest commit**
2. Aguarde o build terminar (~2-5 min)

### Passo 4: Verificar Logs

Abra **Logs** e procure por:
```
✅ Tabelas criadas com sucesso!
✅ Conexão com banco OK - X usuários existentes
✅ Banco de dados inicializado!
🌐 CORS Origins configuradas: [...]
🌟 Starting uvicorn server...
```

**Se aparecer:**
```
❌ ERRO FATAL ao inicializar banco de dados
```
→ O deploy vai **falhar de propósito** (é o comportamento correto agora). Copie o erro e me envie.

---

## 🧪 Testes Após Deploy

### Teste 1: Health Check
```bash
curl https://bioacess.onrender.com/health
```
**Esperado:**
```json
{"status":"ok"}
```

### Teste 2: Preflight CORS (OPTIONS)
```bash
curl -i -X OPTIONS 'https://bioacess.onrender.com/auth/login' \
  -H 'Origin: https://bio-acess.vercel.app' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type'
```

**Esperado:**
```
HTTP/2 200
access-control-allow-origin: https://bio-acess.vercel.app
access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
access-control-allow-headers: content-type
```

### Teste 3: Login Real (POST)
```bash
curl -i -X POST 'https://bioacess.onrender.com/auth/login' \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://bio-acess.vercel.app' \
  -d '{"username":"ana.luiza","password":"senha123"}'
```

**Esperado:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "role": "public",
  "clearance_level": 1,
  "username": "ana.luiza"
}
```

### Teste 4: Frontend (Bio-Acess Vercel)

1. Abra https://bio-acess.vercel.app
2. Console do browser: **NÃO deve ter erros CORS**
3. Tente login com `ana.luiza` / `senha123`
4. Se retornar 500, abra Render Logs e copie o stacktrace completo

---

## 🐛 Se Ainda Houver Erros

### Erro: "Field required [type=missing, input_value=...]"
→ Faltou definir variável no Render. Veja **Passo 2** acima.

### Erro: "No 'Access-Control-Allow-Origin' header"
→ O CORS ainda não carregou. Verifique se o deploy usou o código novo:
```bash
# Nos logs, deve aparecer:
🌐 CORS Origins configuradas: [...]
```

### Erro 500 em `/auth/login`
→ Problema no banco ou lógica de autenticação. **Me envie:**
1. Stacktrace completo dos logs do Render
2. Payload que você enviou (JSON do POST)

---

## 📊 Arquivos Modificados

| Arquivo | Mudança |
|---------|---------|
| `src/backend/app/config.py` | Tornou `SUPABASE_DB_URL` opcional, adicionou defaults |
| `src/backend/app/main.py` | Adicionou exception handler global + logging |
| `render_start.py` | Melhorou inicialização do DB, para em caso de erro |
| `render.yaml` | Corrigiu formato do `CORS_ORIGINS` (CSV, não JSON) |

---

## 🎯 Próximos Passos (se tudo funcionar)

1. **Testar frontend completo** (login, cadastro, biometria)
2. **Remover origens de localhost do CORS** em produção
3. **Configurar domínio customizado** (opcional)
4. **Monitorar performance** no Render Dashboard
5. **Configurar variáveis de ambiente secretas** (JWT_SECRET forte)

---

**Qualquer problema, me chame! 🚀**
