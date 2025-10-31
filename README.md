
# BioAccess - Sistema de Autenticação Biométrica Facial

Sistema completo de autenticação biométrica facial para controle de acesso multinível, desenvolvido para o Ministério do Meio Ambiente.

## 🚀 Funcionalidades

- **Autenticação Biométrica**: Reconhecimento facial usando DeepFace + Facenet512
- **Controle de Acesso Multinível**: 3 níveis de clearance (Público, Diretor, Ministro)
- **Interface Web Moderna**: React + TypeScript com componentes UI elegantes
- **API RESTful**: FastAPI com documentação automática
- **Banco de Dados**: Supabase PostgreSQL para produção
- **Detecção de Vivacidade**: Anti-spoofing para maior segurança

## 📋 Contexto - Atividade Prática Supervisionada (APS)

### 🎯 Objetivo do Sistema
Desenvolver uma ferramenta de **identificação e autenticação biométrica** que restrinja o acesso a uma rede com banco de dados do **Ministério do Meio Ambiente**, contendo informações estratégicas sobre:

- **Propriedades rurais** que utilizam **agrotóxicos proibidos**
- **Impactos ambientais** em lençóis freáticos, rios e mares
- **Dados classificados** por níveis de segurança governamental

### � Níveis de Acesso Implementados

| Nível | Perfil de Acesso | Dados Disponíveis |
|-------|------------------|-------------------|
| **Nível 1** | 👥 **Acesso Público** | Informações básicas e estatísticas gerais sobre agrotóxicos |
| **Nível 2** | 👨‍💼 **Diretores de Divisões** | Relatórios detalhados de propriedades infratoras por região |
| **Nível 3** | 🏛️ **Ministro do Meio Ambiente** | Acesso total: dados sensíveis, estratégias e operações em andamento |

### 🛡️ Funcionalidades de Segurança

- **Autenticação Biométrica Facial**: Reconhecimento facial para identificação única
- **Detecção de Liveness**: Previne ataques com fotos estáticas usando múltiplas capturas
- **Controle de Acesso Hierárquico**: Validação rigorosa de clearance por nível
- **Auditoria Governamental**: Log completo de todas as tentativas de acesso
- **Aquisição Múltipla de Imagem**: Suporte a câmera, scanner, arquivos de imagem e vídeo

## 🏗️ Arquitetura do Sistema

### Frontend (React + TypeScript + Vite)

- **Framework**: React 18 com TypeScript
- **Build Tool**: Vite 6
- **UI Components**: shadcn/ui (Radix UI + Tailwind CSS)
- **Roteamento**: React Router v6
- **Estado Global**: Context API
- **Captura de Mídia**: WebRTC (getUserMedia)

### Backend (FastAPI + Python)

- **Framework**: FastAPI com SQLAlchemy
- **Banco de Dados**: PostgreSQL (com Supabase)
- **Processamento Biométrico**: DeepFace ou face_recognition
- **Autenticação**: JWT tokens
- **Detecção de Liveness**: Análise de múltiplas imagens

## 🚀 Executando o Projeto

### Pré-requisitos

- Node.js 18+ 
- Python 3.9+
- PostgreSQL (ou Supabase)

### Frontend

```bash
# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev

# Build para produção
npm run build
```

### Backend

```bash
cd src/backend

# Instalar dependências Python
pip install -r requirements.txt

# Executar servidor FastAPI
python -m uvicorn app.main:app --reload --port 8000
```

## 🔐 Níveis de Acesso

| Nível | Papel | Descrição |
|-------|-------|-----------|
| **1** | Público | Acesso básico a informações públicas |
| **2** | Diretor | Acesso a dados de diretoria |
| **3** | Ministro | Acesso total do sistema |

## 📱 Funcionalidades

### ✅ Implementadas (Frontend)

- **Interface de Login**: Entrada de usuário + captura biométrica
- **Cadastro Biométrico**: Enroll de nova biometria facial
- **Dashboard**: Painel principal com informações do usuário
- **Controle de Acesso**: Rotas protegidas por nível
- **Relatórios**: Interface para visualizar logs de auditoria
- **Captura de Liveness**: Dois cliques para validação
- **Design Responsivo**: Interface adaptativa

### ✅ Implementadas (Backend - Parcial)

- **Estrutura FastAPI**: App principal configurado
- **Modelos de Dados**: SQLAlchemy models
- **Rotas Base**: Estrutura dos endpoints
- **Configuração**: Settings e CORS
- **Serviços Base**: Estrutura dos services

## ⚠️ **FALTANDO NO BACKEND** - Para o Teles

### 🔧 Implementações Critical Missing

#### 1. **Serviços de Processamento Biométrico**

**Arquivo**: `src/backend/app/services/biometric_engine.py`

**Faltando**:
- ✅ Estrutura base criada
- ❌ **Função `extract_embedding()`** - Extrair features faciais da imagem
- ❌ **Função `verify_match()`** - Comparar embeddings para autenticação
- ❌ **Tratamento de erros** para imagens inválidas
- ❌ **Otimização de performance** do processamento

#### 2. **Detecção de Liveness**

**Arquivo**: `src/backend/app/services/liveness.py`

**Status**: ❌ **COMPLETAMENTE FALTANDO**

**Precisa implementar**:
```python
def validate_liveness(image_a_b64: str, image_b_b64: str) -> bool:
    """
    Valida se as duas imagens são de uma pessoa real
    - Compara diferenças entre as duas capturas
    - Detecta movimento facial mínimo
    - Previne ataques com fotos estáticas
    """
    pass
```

#### 3. **Sistema de Auditoria**

**Arquivo**: `src/backend/app/services/audit.py`

**Status**: ❌ **COMPLETAMENTE FALTANDO**

**Precisa implementar**:
```python
def log_action(db: Session, user: str, action: str, 
               level: int, success: bool, ip: str):
    """
    Grava logs de todas as ações no sistema
    - Login attempts
    - Data access por nível
    - Tentativas falhadas
    """
    pass
```

#### 4. **Endpoints de Autenticação**

**Arquivo**: `src/backend/app/routers/auth.py`

**Faltando**:
- ❌ **Lógica completa do `/auth/enroll`**
- ❌ **Lógica completa do `/auth/verify`**
- ❌ **Tratamento de erros HTTP adequado**
- ❌ **Validação de entrada (Pydantic)**

#### 5. **Endpoints de Dados**

**Arquivo**: `src/backend/app/routers/data.py`

**Status**: ❌ **COMPLETAMENTE FALTANDO**

**Precisa implementar**:
```python
@router.get("/level/{level}")
async def get_level_data(level: int, token: dict = Depends(verify_token)):
    """
    Retorna dados baseado no nível de clearance
    - Valida se usuário tem acesso ao nível
    - Retorna dados mock ou reais
    """
    pass
```

#### 6. **Endpoints de Relatórios**

**Arquivo**: `src/backend/app/routers/reports.py`

**Status**: ❌ **COMPLETAMENTE FALTANDO**

**Precisa implementar**:
```python
@router.get("/audit")
async def get_audit_logs(params: AuditParams, token: dict = Depends(verify_token)):
    """
    Retorna logs de auditoria com filtros
    - Paginação
    - Filtros por data, ação, sucesso
    - Somente para níveis 2 e 3
    """
    pass
```

#### 7. **Sistema de Segurança JWT**

**Arquivo**: `src/backend/app/security.py`

**Faltando**:
- ❌ **Função `create_access_token()`**
- ❌ **Função `verify_token()`** 
- ❌ **Middleware de autenticação**
- ❌ **Validação de clearance por nível**

#### 8. **Database Setup**

**Arquivo**: `src/backend/app/db.py`

**Faltando**:
- ❌ **Conexão com PostgreSQL/Supabase**
- ❌ **Configuração de sessões**
- ❌ **Função `get_db()` dependency**

#### 9. **Modelos Completos**

**Arquivo**: `src/backend/app/models.py`

**Faltando**:
- ❌ **Modelo `AuditLog`** completo
- ❌ **Relacionamentos entre tabelas**
- ❌ **Índices para performance**

#### 10. **Configurações**

**Arquivo**: `src/backend/app/config.py`

**Faltando**:
- ❌ **Variáveis de ambiente**
- ❌ **Configuração de banco**
- ❌ **Secrets JWT**

### 📋 **Especificação Completa**

O arquivo `src/BACKEND_SPEC.md` contém **especificações detalhadas** de como implementar cada endpoint e função. Use como referência!

### 🗄️ **Banco de Dados**

Esquema SQL disponível em: `src/backend/infra/supabase_schema.sql`

### 🧪 **Testes**

Estrutura de testes em: `src/backend/tests/`

**Precisa implementar**:
- Testes unitários para cada serviço
- Testes de integração para endpoints
- Mocks para processamento biométrico

## 🔗 **APIs Frontend → Backend**

O frontend já está **100% pronto** e faz chamadas para estas APIs:

### Endpoints Esperados:

```typescript
// Cadastro de biometria
POST /auth/enroll
{
  "username": "string",
  "image_b64": "base64_image"
}

// Login com liveness
POST /auth/verify  
{
  "username": "string",
  "image_b64_a": "base64_image",
  "image_b64_b": "base64_image"
}

// Acesso a dados por nível
GET /data/level/{level}
Headers: { Authorization: "Bearer <token>" }

// Logs de auditoria
GET /reports/audit?page=1&limit=50
Headers: { Authorization: "Bearer <token>" }
```

## 🎯 **Próximos Passos para o Teles**

1. **Configurar ambiente Python** com as dependências
2. **Implementar os serviços core** (biometric_engine, liveness, audit)
3. **Completar os endpoints** seguindo a especificação
4. **Configurar banco de dados** PostgreSQL/Supabase
5. **Testar integração** com o frontend
6. **Implementar testes** unitários

## 📞 **Contato**

- **Frontend**: Ana Luiza (✅ Completo)
- **Backend**: Teles (⚠️ Pendente implementação)

---

**Projeto criado**: Outubro 2025  

O frontend está 100% funcional e aguarda apenas a implementação do backend! 🚀
  