"""Aplicação principal FastAPI do BioAccess"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, data, reports

app = FastAPI(
    title="BioAccess API",
    description="Sistema de Autenticação Biométrica Facial com Controle de Acesso por Níveis (RBAC)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS para permitir frontend
import os
import json

# Lê CORS_ORIGINS do ambiente (JSON ou CSV)
cors_env = os.getenv("CORS_ORIGINS")
allowed_origins = ["*"]  # Permite todas as origens temporariamente

if cors_env:
    try:
        allowed_origins = json.loads(cors_env)
        print(f"✅ CORS configurado via JSON: {allowed_origins}")
    except Exception as e:
        print(f"⚠️ Erro ao parsear JSON, usando CSV: {e}")
        allowed_origins = [o.strip() for o in cors_env.split(",") if o.strip()]
        print(f"✅ CORS configurado via CSV: {allowed_origins}")
else:
    print("⚠️ CORS_ORIGINS não definido, usando configuração padrão permissiva")

print(f"🌐 CORS Origins configuradas: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Registra routers
app.include_router(auth.router)
app.include_router(data.router)
app.include_router(reports.router)


@app.get("/")
async def root():
    """Endpoint raiz - informações da API"""
    cors_env = os.getenv("CORS_ORIGINS", "not_set")
    return {
        "message": "BioAccess API - Sistema de Autenticação Biométrica Facial",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "cors_enabled": True,
        "cors_origins_env": cors_env,
        "cors_origins_active": allowed_origins
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
