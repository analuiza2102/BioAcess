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

# Domínios permitidos (desenvolvimento + produção)
allowed_origins = [
    "http://localhost:3003",
    "http://localhost:3002", 
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3003",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:3001", 
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173"
]

# Adicionar domínio de produção se especificado
frontend_url = os.getenv('FRONTEND_URL')
if frontend_url:
    allowed_origins.append(frontend_url)

# Permitir todos os domínios .vercel.app em produção
if os.getenv('NODE_ENV') == 'production':
    allowed_origins.append("https://*.vercel.app")

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
            "http://localhost:5173"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
