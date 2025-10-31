# BioAccess Backend

Sistema de Autenticação Biométrica Facial com controle de acesso baseado em níveis (RBAC + JWT).

## 🎯 Visão Geral

O backend do BioAccess implementa:

- **Autenticação biométrica facial** usando DeepFace/Facenet
- **Detecção de vivacidade (liveness)** com duas capturas
- **Controle de acesso por níveis** (1/2/3) usando RBAC
- **JWT** para sessões autenticadas
- **Logs de auditoria completos** de todas as ações
- **Integração com Supabase** (PostgreSQL)

## 📋 Requisitos

- Python 3.9+
- PostgreSQL (Supabase)
- Webcam (para captura biométrica no frontend)

## 🚀 Instalação

### 1. Clone o repositório

```bash
cd backend
```

### 2. Crie ambiente virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale dependências

```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais:

```env
SUPABASE_DB_URL=postgresql://user:password@db.xxxx.supabase.co:5432/postgres
JWT_SECRET=seu-secret-super-secreto-aqui-mude-em-producao
```

### 5. Configure banco de dados

Execute o script SQL no Supabase SQL Editor:

```bash
cat infra/supabase_schema.sql
```

Isso criará:
- Tabelas: `users`, `biometric_templates`, `audit_logs`
- Usuários de teste: `alice` (nível 1), `bruno` (nível 2), `ministro` (nível 3)

## ▶️ Executar

### Modo desenvolvimento

```bash
uvicorn app.main:app --reload --port 8000
```

### Modo produção

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Acesse:
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

## 📡 Endpoints

### Autenticação

**POST /auth/enroll**
```json
{
  "username": "alice",
  "image_b64": "data:image/png;base64,..."
}
```

**POST /auth/verify**
```json
{
  "username": "alice",
  "image_b64_a": "data:image/png;base64,...",
  "image_b64_b": "data:image/png;base64,..."
}
```

### Dados por Nível

**GET /data/level/{level}**
- Headers: `Authorization: Bearer <token>`
- Níveis: 1, 2, 3

### Relatórios (apenas clearance 3)

**GET /reports/audit**
- Headers: `Authorization: Bearer <token>`
- Query params: `page`, `limit`, `start_date`, `end_date`, `action`, `success`

## 🧪 Testes

```bash
pytest tests/
```

## 🔐 Segurança

### Níveis de Clearance

1. **Nível 1 (público)**: Todos os usuários autenticados
2. **Nível 2 (diretor)**: Diretores de divisões
3. **Nível 3 (ministro)**: Acesso total + relatórios de auditoria

### Autenticação JWT

- Tokens expiram em 30 minutos (configurável)
- Algoritmo: HS256
- Claims: `sub` (username), `exp` (expiração)

### Liveness Detection

Valida que a captura é de uma pessoa viva (não foto/vídeo):
- Duas capturas com pequena variação
- Embeddings devem ser similares mas não idênticos
- Diferença entre 0.05 e 0.25 (configurável)

## 📊 Auditoria

Todas as ações são registradas:
- Tentativas de enroll e verify (sucesso/falha)
- Acessos a cada nível de dados
- IP de origem
- Timestamp

## 🗄️ Estrutura do Banco

```sql
users
  - id (PK)
  - username (unique)
  - role (public/director/minister)
  - clearance (1/2/3)
  - password_hash
  - created_at

biometric_templates
  - id (PK)
  - user_id (FK -> users)
  - embedding (JSONB)
  - created_at

audit_logs
  - id (PK)
  - user
  - action
  - level_requested
  - success
  - origin_ip
  - ts
```

## 🔧 Configurações

Arquivo `.env`:

```env
# Database
SUPABASE_DB_URL=postgresql://...

# JWT
JWT_SECRET=secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173

# Biometria
EMBEDDING_MODEL=Facenet
SIMILARITY_THRESHOLD=0.6

# Liveness
LIVENESS_EMBEDDING_DIFF_MIN=0.05
LIVENESS_EMBEDDING_DIFF_MAX=0.25
```

## 📦 Tecnologias

- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM para PostgreSQL
- **DeepFace**: Reconhecimento facial (Facenet)
- **python-jose**: JWT
- **passlib**: Hashing de senhas
- **Supabase**: PostgreSQL cloud

## 🎓 Contexto Acadêmico

Este sistema foi desenvolvido como parte de trabalho acadêmico sobre:
- **PIVC** (Processamento de Imagens e Visão Computacional)
- **Segurança da Informação** (JWT, RBAC, LGPD)
- **Banco de Dados** (PostgreSQL, auditoria)
- **Engenharia de Software** (arquitetura, testes)

## 📝 Licença

MIT

## 👥 Contribuição

Desenvolvido para o Ministério do Meio Ambiente (contexto acadêmico).
