"""Configurações e variáveis de ambiente do BioAccess"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    SUPABASE_DB_URL: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3003,http://localhost:3002,http://localhost:3000,http://localhost:3001,http://localhost:5173"
    
    # Biometria
    EMBEDDING_MODEL: str = "Facenet"  # Facenet, VGG-Face, OpenFace
    SIMILARITY_THRESHOLD: float = 0.6
    
    # Liveness
    LIVENESS_EMBEDDING_DIFF_MIN: float = 0.05
    LIVENESS_EMBEDDING_DIFF_MAX: float = 0.25

    # Demo mode (simulated biometric processing)
    DEMO_MODE: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Tentar carregar configurações
try:
    settings = Settings()
except Exception as e:
    print(f"Erro ao carregar configurações: {e}")
    print("🔧 Usando configurações padrão para modo demo...")
    
    # Configurações padrão para desenvolvimento
    import os
    
    # Configurar variáveis de ambiente padrão
    os.environ.setdefault('DEMO_MODE', 'true')
    os.environ.setdefault('SUPABASE_DB_URL', 'sqlite:///./meio_ambiente.db')
    os.environ.setdefault('JWT_SECRET', 'demo_secret_key_aps_2024')
    os.environ.setdefault('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003')
    
    # Tentar carregar novamente com configurações padrão
    try:
        settings = Settings()
        print("✅ Configurações carregadas com sucesso usando padrões")
    except Exception as e2:
        print(f"❌ Erro crítico nas configurações: {e2}")
        # Configuração mínima hardcoded para demo
        class FallbackSettings:
            DEMO_MODE = True
            SUPABASE_DB_URL = "sqlite:///./meio_ambiente.db"
            JWT_SECRET = "demo_secret_key_aps_2024"
            JWT_ALGORITHM = "HS256"
            JWT_EXPIRATION_MINUTES = 30
            CORS_ORIGINS = "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003"
            SIMILARITY_THRESHOLD = 0.3  # Mais permissivo para demo
            LIVENESS_EMBEDDING_DIFF_MIN = 0.02
            LIVENESS_EMBEDDING_DIFF_MAX = 0.4
            EMBEDDING_MODEL = "Facenet"
        
        settings = FallbackSettings()
        print("🆘 Usando configurações de emergência")
