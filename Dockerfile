# Dockerfile customizado para Railway - APENAS Python Backend

FROM python:3.11-slim

# Instalar dependências do sistema para OpenCV e face_recognition
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar apenas os arquivos do backend
COPY requirements.txt .
COPY start.py .
COPY runtime.txt .
COPY src/backend/ ./src/backend/

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Expor porta
EXPOSE 8001

# Comando de inicialização
CMD ["python", "start.py"]
