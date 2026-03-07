# Use Python official image# Multi-stage build para otimizar imagem








































CMD ["python", "run.py"]# Run applicationEXPOSE 5000# Expose port    CMD python -c "import requests; requests.get('http://localhost:5000/health')"HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \# Health checkUSER appuserRUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app# Create non-root user for securityCOPY . .# Copy application    pip install -r requirements.txtRUN pip install --upgrade pip setuptools wheel && \# Install Python dependenciesCOPY config/requirements.txt .# Copy requirements    && rm -rf /var/lib/apt/lists/*    postgresql-client \    gcc \RUN apt-get update && apt-get install -y --no-install-recommends \# Install system dependenciesENV PIP_NO_CACHE_DIR=1ENV PYTHONUNBUFFERED=1ENV PYTHONDONTWRITEBYTECODE=1# Set environment variablesWORKDIR /app# Set working directoryFROM python:3.10-slim
FROM python:3.10-slim as builder

WORKDIR /app

# Instalar dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY config/requirements.txt .

# Criar requirements compilado
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage final
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências de runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar wheels do builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache /wheels/*

# Copiar aplicação
COPY . .

# Criar usuário não-root
RUN useradd -m -u 1000 loto && chown -R loto:loto /app
USER loto

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expor porta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=run.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# Comando padrão
CMD ["python", "run.py"]
