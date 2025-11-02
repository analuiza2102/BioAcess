# BioAccess Backend (fixed)

Backend FastAPI com CORS configurado corretamente e endpoint de login por JSON.

## Como rodar localmente

```bash
python -m venv .venv
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
# Linux/Mac:
# source .venv/bin/activate
pip install -r requirements.txt

# variáveis (opcional)
export JWT_SECRET_KEY="troque-isto"
export DATABASE_URL="sqlite:///./bioaccess.db"
export CORS_ORIGINS='["http://localhost:5173","https://bio-acess.vercel.app"]'

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse: http://localhost:8000/docs

## Teste rápido

Um usuário demo é criado automaticamente (apenas se não existir):
- username: `ana.luiza`
- senha: `admin123`

```bash
curl -X POST http://localhost:8000/auth/login   -H "Content-Type: application/json"   -d '{"username":"ana.luiza","password":"admin123"}'
```

## Deploy (Render)

- Start Command:
  ```
  gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app
  ```

- Environment:
  ```
  JWT_SECRET_KEY=<sua chave segura>
  DATABASE_URL=<postgres ou sqlite>
  CORS_ORIGINS=["https://bio-acess.vercel.app","http://localhost:5173"]
  ```

## Observações
- O endpoint `/auth/login` aceita **JSON**.
- Se preferir `form-data` (OAuth2), ajuste o `auth.py` conforme necessidade.
