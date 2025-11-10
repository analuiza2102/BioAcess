# BioAccess Backend

Backend FastAPI com reconhecimento facial usando face_recognition (dlib).

## Como rodar localmente

```bash
python -m venv .venv
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
# Linux/Mac:
# source .venv/bin/activate
pip install -r requirements.txt

# Variáveis de ambiente necessárias
# Criar arquivo .env na raiz do projeto com:
SUPABASE_DB_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
JWT_SECRET=sua-chave-secreta
CORS_ORIGINS=http://localhost:5173,https://bio-acess.vercel.app

# Iniciar servidor
python start.py
```

Acesse: http://localhost:8000/docs

## Teste rápido

Usuários demo são criados automaticamente:
- username: `ana.luiza` / senha: `senha123`
- username: `teste1` / senha: `teste123`
- username: `diretor.silva` / senha: `diretor2024` (clearance 2)
- username: `ministro.ambiente` / senha: `ministro2024` (clearance 3)

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"ana.luiza","password":"senha123"}'
```

## Deploy (Railway)

Veja o guia completo: `RAILWAY_DEPLOY.md` na raiz do projeto.

**Quick Start**:
1. Conecte repositório no Railway
2. Configure variáveis de ambiente
3. Deploy automático!

## Observações
- Reconhecimento facial usa face_recognition (dlib) - mais leve e estável
- Requer ~200MB RAM (muito mais leve que TensorFlow)
- Precisão de 99.38% em detecção facial
- Se preferir `form-data` (OAuth2), ajuste o `auth.py` conforme necessidade.
