import os, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, data, reports

app = FastAPI(
    title="BioAccess API",
    description="Sistema de Autenticação Biométrica Facial com Controle de Acesso (RBAC)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---- CORS ----
default_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://bio-acess.vercel.app",
    "https://bio-acess-o7ra1en0k-ana-luiza-guimaraes-luizaos-projects.vercel.app",
]

cors_env = os.getenv("CORS_ORIGINS", "").strip()
env_origins = []
if cors_env:
    try:
        env_origins = json.loads(cors_env) if cors_env.startswith("[") else [o.strip() for o in cors_env.split(",") if o.strip()]
    except Exception:
        env_origins = [o.strip() for o in cors_env.split(",") if o.strip()]

allowed_origins = list(dict.fromkeys([*default_origins, *env_origins]))

print("🌐 CORS Origins configuradas:", allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ---- Routers ----
app.include_router(auth.router)
app.include_router(data.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"ok": True, "service": "BioAccess API", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
