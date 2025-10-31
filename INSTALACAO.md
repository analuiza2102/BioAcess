# 🚀 INSTALAÇÃO RÁPIDA - BioAccess

## ⚡ Início Rápido (3 passos)

### 1️⃣ **Frontend (React)**
```bash
npm install
npm run dev
# ➜ http://localhost:3000
```

### 2️⃣ **Backend (FastAPI)**  
```bash
cd src/backend
pip install -r requirements.txt

# Configurar .env (copie de .env.example)
cp .env.example .env
# Edite .env com suas credenciais Supabase

# Iniciar servidor
python run_server.py
# ➜ http://localhost:8001
# ➜ API Docs: http://localhost:8001/docs
```

### 3️⃣ **Inicialização Automática**
```bash
# Script que configura tudo automaticamente
python start_bioaccess.py
```

## 👤 Login de Teste

**Usuário:** ana.luiza  
**Senha:** 123456  
**Biometria:** ✅ Cadastrada

## 🔧 URLs Importantes

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001  
- **Documentação:** http://localhost:8001/docs
- **Login:** http://localhost:3000/login

## 📁 Estrutura Limpa

```
BioAccess Setup/
├── src/
│   ├── backend/          # API FastAPI
│   ├── components/       # Componentes React  
│   ├── pages/           # Páginas web
│   └── lib/             # Utilitários
├── start_bioaccess.py   # Script de inicialização
├── package.json         # Dependências frontend
└── README.md           # Documentação completa
```

## ✅ Sistema Pronto para Uso!

Todos os arquivos de teste e desenvolvimento foram removidos.  
Apenas código de produção e configurações essenciais mantidos.