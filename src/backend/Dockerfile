FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /backend

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements_production.txt ./
RUN pip install --no-cache-dir -r requirements_production.txt

# Copiar todo o código do backend
COPY . ./

# Expor porta
EXPOSE 8001

# Usar run_server.py que já funciona localmente
CMD ["python", "run_server.py"]