# 🔧 GUIA DE CONFIGURAÇÃO DO .env - BioAccess

## 📋 **O que você precisa configurar**

### 1️⃣ **SUPABASE_DB_URL** (Banco de Dados)
**O que é:** URL de conexão com o banco PostgreSQL do Supabase  
**Formato:** `postgresql://postgres:[SENHA]@db.[PROJECT-REF].supabase.co:5432/postgres`

#### **Como obter:**
1. Acesse: https://supabase.com/dashboard
2. Entre no seu projeto ou crie um novo
3. Vá em **Settings** → **Database**
4. Procure por **"Connection string"** ou **"URI"**
5. Copie a URL que aparece (já inclui senha)

#### **Exemplo atual:**
```
SUPABASE_DB_URL=postgresql://postgres:qYfLVRxCw7LFMetP@db.krutpwnvwfynylefapeh.supabase.co:5432/postgres
```

#### **Para desenvolvimento local (alternativa):**
```
SUPABASE_DB_URL=sqlite:///./meio_ambiente.db
```

---

### 2️⃣ **JWT_SECRET** (Segurança)
**O que é:** Chave secreta para assinar tokens de autenticação  
**Requisitos:** Mínimo 32 caracteres, caracteres aleatórios

#### **Como gerar:**
**Opção 1 - Online:**
- Acesse: https://randomkeygen.com/
- Use "CodeIgniter Encryption Keys" (256-bit)

**Opção 2 - Python:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Opção 3 - PowerShell:**
```powershell
-join ((1..32) | ForEach {Get-Random -input ([char[]]'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')})
```

#### **Exemplo:**
```
JWT_SECRET=mK9vR2nQ8xP5dL7fJ3hB6wE1yT4uI0oA8sD9gF2hJ5kL
```

---

### 3️⃣ **Configurações de Biometria** (Opcional)

#### **BIOMETRIC_THRESHOLD** 
- **Padrão:** 0.6
- **Valores:** 0.0 (permissivo) a 1.0 (rigoroso)
- **Recomendado:** 0.6 para produção, 0.3 para testes

#### **LIVENESS_ENABLED**
- **Padrão:** true
- **Valores:** true (ativo) / false (desabilitado)

---

### 4️⃣ **Configurações da API** (Opcional)

#### **DEBUG**
- **Desenvolvimento:** true
- **Produção:** false

#### **CORS_ORIGINS**
- URLs permitidas para acesso
- **Padrão:** `["http://localhost:3000","http://localhost:5173"]`

#### **API_PORT**
- **Padrão:** 8001
- Porta onde o servidor FastAPI vai rodar

---

## 📝 **TEMPLATE COMPLETO PARA SEU .env**

Copie e cole no seu arquivo `.env`:

```env
# Configurações do BioAccess - Sistema de Autenticação Biométrica

# ====== BANCO DE DADOS ======
# Cole aqui sua URL do Supabase:
SUPABASE_DB_URL=postgresql://postgres:SUA_SENHA_AQUI@db.SEU_PROJECT_REF.supabase.co:5432/postgres

# ====== SEGURANÇA JWT ======  
# Gere uma chave de 32+ caracteres:
JWT_SECRET=GERE_UMA_CHAVE_SECRETA_ALEATORIA_DE_32_CARACTERES_MINIMO

# ====== CONFIGURAÇÕES DE BIOMETRIA ======
# Modelo de embedding (Facenet, VGG-Face, OpenFace)
EMBEDDING_MODEL=Facenet512
# Limiar de similaridade (0.3=permissivo, 0.6=normal, 0.8=rigoroso)
SIMILARITY_THRESHOLD=0.6

# ====== CONFIGURAÇÕES DE LIVENESS ======
# Diferença mínima entre embeddings (anti-spoofing)
LIVENESS_EMBEDDING_DIFF_MIN=0.01
# Diferença máxima entre embeddings
LIVENESS_EMBEDDING_DIFF_MAX=0.4

# ====== CONFIGURAÇÕES DA API ======
# URLs permitidas para CORS (separadas por vírgula)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# ====== MODO DEMO ======
# false=usa DeepFace real, true=simulação
DEMO_MODE=false
```

---

## 🚀 **PASSO A PASSO RÁPIDO**

1. **Copie o .env.example:**
   ```bash
   cd src/backend
   cp .env.example .env
   ```

2. **Edite o arquivo .env:**
   - Substitua `SUA_SENHA_AQUI` pela senha real do Supabase
   - Substitua `SEU_PROJECT_REF` pela referência do seu projeto
   - Gere e coloque um JWT_SECRET

3. **Teste a configuração:**
   ```bash
   python run_server.py
   ```

---

## ✅ **VERIFICAÇÃO**

Se configurado corretamente, você verá:
```
🔧 SUPABASE_DB_URL: postgresql
🔧 JWT_SECRET: CONFIGURADO
🚀 Iniciando BioAccess Backend Real...
```

Se der erro, verifique:
- URL do Supabase está correta
- Senha do banco está certa
- JWT_SECRET tem 32+ caracteres