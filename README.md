
# 🔐 BioAccess - Sistema de Autenticação Biométrica

> **Sistema completo de autenticação biométrica facial para controle de acesso multinível**  

## 🎓 **Contexto Acadêmico**

[![Universidade](https://img.shields.io/badge/Universidade-Ciência%20da%20Computação-blue?style=for-the-badge)](https://github.com/analuiza2102/BioAcess)
[![APS](https://img.shields.io/badge/APS-Atividade%20Prática%20Supervisionada-green?style=for-the-badge)](https://github.com/analuiza2102/BioAcess)
[![Finalidade](https://img.shields.io/badge/Finalidade-Educacional-orange?style=for-the-badge)](https://github.com/analuiza2102/BioAcess)

**Este projeto foi desenvolvido como Atividade Prática Supervisionada (APS) do curso de Ciência da Computação.**

### 📚 **Objetivos Acadêmicos:**
- **Aprendizado Prático**: Implementação de sistema biométrico real
- **Integração de Tecnologias**: Frontend + Backend + Banco de Dados + Deploy
- **Segurança Computacional**: Autenticação, criptografia e controle de acesso
- **Engenharia de Software**: Arquitetura, testes e documentação completa
- **DevOps**: Containerização, CI/CD e deploy em produção

> 💡 **Nota**: Projeto desenvolvido para fins educacionais e demonstração de competências técnicas  

## ✨ Funcionalidades Implementadas

- ✅ **Autenticação Biométrica Completa**: DeepFace + FaceNet512 para reconhecimento facial
- ✅ **Controle de Acesso Multinível**: 3 níveis de clearance (Público, Diretor, Ministro)  
- ✅ **Interface Moderna**: React + TypeScript + Tailwind CSS com Glass Morphism
- ✅ **API RESTful Funcional**: FastAPI com endpoints completos e documentação
- ✅ **Banco de Dados**: Supabase PostgreSQL integrado e funcional
- ✅ **Detecção de Liveness**: Anti-spoofing com dupla captura facial
- ✅ **Sistema de Auditoria**: Logs completos de acesso e tentativas
- ✅ **Responsive Design**: Interface adaptativa para todos os dispositivos
- ✅ **Tema Dark/Light**: Sistema de temas com persistência
- ✅ **Deploy Ready**: Configurado para Railway + Vercel

## 📋 **Atividade Prática Supervisionada (APS) - Ciência da Computação**

### 📖 **Contexto Educacional**
Este projeto foi desenvolvido como **Atividade Prática Supervisionada** do curso de **Ciência da Computação**, com foco em:

- 🔬 **Pesquisa Aplicada**: Estudo de algoritmos de reconhecimento facial
- 💻 **Desenvolvimento Full-Stack**: Frontend + Backend + Database + Deploy
- 🛡️ **Segurança da Informação**: Autenticação biométrica e controle de acesso
- 🏗️ **Arquitetura de Software**: Padrões de projeto e boas práticas
- 🚀 **DevOps**: Containerização, CI/CD e deploy em produção

### 🎯 **Cenário de Aplicação (Fictício para Estudo)**
Sistema de **identificação e autenticação biométrica** para controle de acesso a banco de dados do **Ministério do Meio Ambiente**, contendo informações sobre:

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

### 🎨 Frontend (React + TypeScript + Vite)
- **Framework**: React 18 com TypeScript para type safety
- **Build Tool**: Vite 6 para desenvolvimento rápido  
- **UI Components**: shadcn/ui (Radix UI + Tailwind CSS)
- **Styling**: Tailwind CSS com Glass Morphism design
- **Roteamento**: React Router v6 com rotas protegidas
- **Estado Global**: Context API (Auth + Theme)
- **Captura de Mídia**: WebRTC (getUserMedia) com fallbacks
- **Responsive**: Mobile-first design com breakpoints otimizados

### ⚡ Backend (FastAPI + Python) 
- **Framework**: FastAPI com SQLAlchemy ORM
- **Banco de Dados**: PostgreSQL com Supabase
- **Processamento Biométrico**: DeepFace + TensorFlow + OpenCV
- **Autenticação**: JWT tokens com refresh automático
- **Detecção de Liveness**: Análise de múltiplas capturas com cosine similarity
- **Segurança**: CORS configurado, validação Pydantic, logs de auditoria
- **Deploy**: Dockerfile + Railway/Render ready

### 🛢️ Banco de Dados (Supabase PostgreSQL)
- **Users**: Tabela de usuários com clearance levels
- **Biometric_Templates**: Embeddings faciais encodados
- **Audit_Logs**: Sistema completo de auditoria
- **Índices**: Otimizados para performance de consultas

## 🚀 Deploy em Produção

### 📦 Pré-requisitos Atendidos
- ✅ **Node.js 18+** para desenvolvimento local
- ✅ **Python 3.11** com todas as dependências
- ✅ **Supabase PostgreSQL** configurado e funcional
- ✅ **GitHub Repository** público disponível
- ✅ **Docker** com Dockerfile otimizado
- ✅ **Environment Variables** documentadas

### 🌐 Deploy no Railway (Backend)

**1. Acesse [Railway.app](https://railway.app)**
**2. Deploy from GitHub repo: `analuiza2102/BioAcess`**
**3. Configure as variáveis de ambiente:**

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_service_role_key
JWT_SECRET=sua_chave_jwt_super_secreta_256_bits
ENVIRONMENT=production
```

**4. Deploy Automático:**
- ✅ Railway detecta `Dockerfile` automaticamente
- ✅ Instala dependências Python (`requirements_production.txt`)
- ✅ Configura porta 8001
- ✅ Deploy em ~2-3 minutos

### ☁️ Deploy no Vercel (Frontend)

**1. Acesse [Vercel.com](https://vercel.com)**
**2. Import project: `analuiza2102/BioAcess`**
**3. Configure variável de ambiente:**

```env
VITE_API_URL=https://seu-backend.railway.app
```

**4. Deploy Automático:**
- ✅ Detecção automática do Vite
- ✅ Build otimizado
- ✅ CDN global
- ✅ HTTPS automático

### 💻 Desenvolvimento Local

```bash
# 1. Clone o repositório
git clone https://github.com/analuiza2102/BioAcess.git
cd BioAcess

# 2. Frontend
npm install
npm run dev  # http://localhost:5173

# 3. Backend  
cd src/backend
pip install -r requirements.txt
python run_server.py  # http://localhost:8001

# 4. Launcher (Opcional)
python start_bioaccess.py  # Inicia ambos automaticamente
```

## 🔐 Níveis de Acesso

| Nível | Papel | Descrição |
|-------|-------|-----------|
| **1** | Público | Acesso básico a informações públicas |
| **2** | Diretor | Acesso a dados de diretoria |
| **3** | Ministro | Acesso total do sistema |

## 🎯 Sistema Funcional Completo

### ✅ Frontend (100% Implementado)

- 🎨 **Interface de Login Moderna**: Glass morphism + tema dark/light
- 📷 **Captura Biométrica**: WebRTC com fallbacks para compatibilidade
- 📊 **Dashboard Interativo**: Painel com estatísticas e acesso rápido
- 🔐 **Controle de Acesso**: Rotas protegidas por clearance level
- 📈 **Relatórios Visuais**: Interface para logs de auditoria com filtros
- 🎭 **Detecção de Liveness**: Dupla captura para anti-spoofing
- 📱 **Design Responsivo**: Mobile-first com breakpoints otimizados
- 🌓 **Sistema de Temas**: Persistência de preferências
- ⚡ **Performance**: Lazy loading + code splitting

### ✅ Backend (100% Implementado)

- 🚀 **API FastAPI Completa**: Todos os endpoints funcionais
- 🧠 **DeepFace Integration**: Reconhecimento facial real
- 🛡️ **Sistema JWT**: Autenticação + refresh tokens
- 🔍 **Liveness Detection**: Algoritmo cosine similarity
- 📝 **Sistema de Auditoria**: Logs detalhados de todas as ações
- 🗄️ **Supabase Integration**: PostgreSQL com ORM
- 🐳 **Docker Ready**: Containerização completa
- 🔒 **Security**: CORS + validação + sanitização

## 🚀 Status do Projeto

### 📊 Progresso Completo: 100% ✅

| Componente | Status | Funcionalidades |
|------------|--------|-----------------|
| 🎨 **Frontend** | ✅ **100%** | Interface, temas, responsividade, captura de câmera |
| ⚡ **Backend** | ✅ **100%** | APIs, autenticação, biometria, liveness, auditoria |
| 🗄️ **Database** | ✅ **100%** | Supabase configurado, tabelas, relacionamentos |
| 🔐 **Security** | ✅ **100%** | JWT, CORS, validação, sanitização |
| 🐳 **Deploy** | ✅ **100%** | Dockerfile, Railway config, Vercel ready |
| 📱 **Mobile** | ✅ **100%** | Responsive design, touch-friendly |
| 🧪 **Testing** | ✅ **100%** | Testes unitários e de integração |

### 🔧 Principais Implementações

#### 🧠 **Processamento Biométrico**
```python
# src/backend/app/services/biometric_engine.py
def extract_embedding(image_b64: str) -> np.ndarray:
    """Extração de features faciais com DeepFace + FaceNet512"""
    
def verify_match(embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
    """Comparação de embeddings com cosine similarity"""
```

#### 🎭 **Detecção de Liveness**
```python  
# src/backend/app/services/liveness.py
def validate_liveness(image_a_b64: str, image_b_b64: str) -> bool:
    """Validação anti-spoofing com análise de diferenças entre capturas"""
```

#### 📝 **Sistema de Auditoria**
```python
# src/backend/app/services/audit.py  
def log_action(db: Session, user_id: str, action: str, level: int, 
               success: bool, ip_address: str, details: dict):
    """Sistema completo de logs para compliance governamental"""
```

#### 🔐 **Endpoints de Autenticação**  
```python
# src/backend/app/routers/auth.py
@router.post("/enroll")  # Cadastro biométrico
@router.post("/verify")  # Login com liveness
@router.post("/check-biometric")  # Verificação rápida
```

#### 📊 **Endpoints de Dados por Nível**
```python
# src/backend/app/routers/data.py
@router.get("/level/{level}")  # Dados por clearance
@router.get("/user-info")  # Informações do usuário
```

#### 📈 **Endpoints de Relatórios**
```python
# src/backend/app/routers/reports.py
@router.get("/audit")  # Logs de auditoria paginados
@router.get("/statistics")  # Estatísticas do sistema
```

### 🗄️ **Banco de Dados Configurado**

**Tabelas Implementadas:**
- ✅ `users` - Usuários com clearance levels
- ✅ `biometric_templates` - Embeddings faciais 
- ✅ `audit_logs` - Sistema de auditoria completo
- ✅ `system_config` - Configurações do sistema

### 🧪 **Testes Implementados**

- ✅ **Testes Unitários**: Serviços e funções críticas
- ✅ **Testes de Integração**: Endpoints e fluxos completos  
- ✅ **Testes de Performance**: Processamento biométrico
- ✅ **Mocks**: DeepFace e dependências externas

## 🔗 APIs Funcionais

### 📡 Endpoints Implementados e Testados

```typescript
// 🔐 Autenticação
POST /auth/enroll          // ✅ Cadastro biométrico funcionando
POST /auth/verify          // ✅ Login com liveness funcionando  
POST /auth/check-biometric // ✅ Verificação rápida funcionando

// 📊 Dados por Nível de Acesso
GET /data/level/{level}    // ✅ Retorna dados por clearance
GET /data/user-info        // ✅ Informações do usuário logado

// 📈 Relatórios e Auditoria  
GET /reports/audit         // ✅ Logs paginados com filtros
GET /reports/statistics    // ✅ Estatísticas do sistema
```

### 🔄 Fluxo Completo Testado

1. **Cadastro**: `POST /auth/enroll` → Embedding salvo no Supabase
2. **Login**: `POST /auth/verify` → Liveness + JWT token 
3. **Acesso**: `GET /data/level/2` → Dados filtrados por clearance
4. **Auditoria**: `GET /reports/audit` → Logs de todas as ações

### 📱 Frontend Integration

O frontend React está **100% integrado** e testado:

```typescript  
// Exemplo de uso real da API
const loginResult = await api.post('/auth/verify', {
  username: 'ana.luiza',
  image_b64_a: captureA,
  image_b64_b: captureB
});

const userData = await api.get('/data/user-info', {
  headers: { Authorization: `Bearer ${token}` }
});
```

## 🎯 Próximos Passos - Deploy Railway

### ⚡ Checklist Pré-Deploy

- ✅ **Código no GitHub**: Repository público disponível
- ✅ **Dockerfile Otimizado**: Backend containerizado 
- ✅ **Dependências**: `requirements_production.txt` completo
- ✅ **Variáveis de Ambiente**: `.env.example` documentado
- ✅ **CORS Configurado**: Produção + desenvolvimento  
- ✅ **Supabase Ready**: Database schema aplicado
- ✅ **Testes Passando**: Todas as funcionalidades validadas

### 🚀 Deploy Instructions

1. **Railway Backend**: Detectará Dockerfile automaticamente
2. **Vercel Frontend**: Build Vite + deploy CDN global  
3. **Environment Variables**: Configurar no Railway dashboard
4. **Domain Setup**: HTTPS automático + custom domain opcional

## 📊 Performance & Security

- 🔒 **Security**: JWT + CORS + Input validation + SQL injection protection
- ⚡ **Performance**: DeepFace optimized + Database indexing + Lazy loading
- 📱 **Mobile**: PWA ready + Touch optimized + Offline capability  
- 🌐 **Internationalization**: i18n ready para múltiplos idiomas

## 👥 **Desenvolvimento Acadêmico**

- 👩‍💻 **Desenvolvido por**: Ana Luiza  
- 🎓 **Curso**: Ciência da Computação
- 📚 **Tipo**: Atividade Prática Supervisionada (APS)
- 🎯 **Objetivo**: Demonstração de competências em desenvolvimento full-stack
- 🏗️ **Escopo**: Sistema completo + Deploy em produção

## 📝 **Considerações Acadêmicas**

> **⚠️ Importante**: Este é um **projeto educacional** desenvolvido para fins de **aprendizado e avaliação acadêmica**. 
> 
> - ✅ **Funcionalidades Reais**: Sistema biométrico completamente funcional
> - 📖 **Finalidade**: Demonstração de conhecimentos técnicos 
> - 🔬 **Tecnologias**: Stack moderno para aprendizado prático
> - 🚀 **Deploy**: Preparado para produção como exercício de DevOps

---

🎓 **Projeto Acadêmico** | **APS - Ciência da Computação** | **Outubro 2025** 🚀
  