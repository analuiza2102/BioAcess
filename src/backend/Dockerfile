FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements_production.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements_production.txt

# Copiar código
COPY app/ ./app/
COPY production_server.py .

# Expor porta
EXPOSE 8001

# Comando de inicialização
CMD ["python", "production_server.py"]