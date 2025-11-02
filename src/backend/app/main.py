"""Aplicação principal FastAPI do BioAccess"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .routers import auth, data, reports
import logging
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bioaccess")

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
import re

# Lê CORS_ORIGINS do ambiente
cors_env = os.getenv("CORS_ORIGINS", "")

# Parse do CORS_ORIGINS (suporta CSV, JSON, ou lista mista)
env_origins = []
if cors_env:
    # Remove caracteres JSON extras se existirem
    cors_env_clean = re.sub(r'[\[\]"\']', '', cors_env)
    # Faz split por vírgula e limpa espaços
    env_origins = [o.strip() for o in cors_env_clean.split(",") if o.strip() and o.strip().startswith("http")]

# Origens padrão para desenvolvimento
default_origins = [
    "http://localhost:5173",
    "https://bio-acess.vercel.app",
]

# Combina origens padrão com as do ambiente (sem duplicatas)
allowed_origins = list(dict.fromkeys([*default_origins, *env_origins]))

print(f"🌐 CORS Origins configuradas: {allowed_origins}")
print(f"🔍 CORS_ORIGINS raw do ambiente: {cors_env}")

# Handler global de exceções
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Captura todas as exceções não tratadas e loga adequadamente"""
    logger.exception(f"Unhandled error on {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "path": str(request.url)
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https://.*\.vercel\.app$",  # Aceita todos os subdomínios do Vercel
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
        "cors_origins_active": allowed_origins,
        "cors_regex_enabled": True
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
