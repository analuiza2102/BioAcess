FROM python:3.11-slim

WORKDIR /app

# Atualizar package lists e instalar dependências básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro para cache do Docker
COPY requirements_production.txt .

# Instalar dependências Python com timeout maior
RUN pip install --no-cache-dir --timeout=1000 -r requirements_production.txt

# Copiar código da aplicação
COPY app/ ./app/
COPY production_server.py .

# Expor porta para Railway
EXPOSE 8001

# Comando de inicialização
CMD ["python", "production_server.py"]