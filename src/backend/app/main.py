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


# Lê CORS_ORIGINS do ambiente (JSON ou CSV)
import json
cors_env = os.getenv("CORS_ORIGINS")
if cors_env:
    try:
        allowed_origins = json.loads(cors_env)
    except Exception:
        allowed_origins = [o.strip() for o in cors_env.split(",") if o.strip()]
else:
    allowed_origins = [
        "http://localhost:3003",
        "http://localhost:3002", 
        "http://localhost:3001",
        "http://localhost:3000",
        "http://localhost:5173",
        "https://bio-acess.vercel.app"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Registra routers
app.include_router(auth.router)
app.include_router(data.router)
app.include_router(reports.router)


@app.get("/")
async def root():
    """Endpoint raiz - informações da API"""
    return {
        "message": "BioAccess API - Sistema de Autenticação Biométrica Facial",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "cors_enabled": True,
        "cors_origins": [
            "http://localhost:3003",
            "http://localhost:3002", 
            "http://localhost:3001",
            "http://localhost:3000",
            "http://localhost:5173",
            "https://bio-acess.vercel.app"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
