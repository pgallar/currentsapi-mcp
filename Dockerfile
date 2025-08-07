FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY requirements.txt .
COPY src/ src/
COPY check-env.sh .
COPY start-server.sh .
COPY healthcheck.sh .

# Dar permisos de ejecución a los scripts
RUN chmod +x check-env.sh start-server.sh healthcheck.sh

# Actualizar pip e instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Crear directorio para logs
RUN mkdir -p logs

# Agregar src al PYTHONPATH
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Configurar variables de entorno para SSE
ENV USE_SSE=true

# Configurar healthcheck
HEALTHCHECK --interval=300s --timeout=30s --start-period=120s --retries=3 CMD ./healthcheck.sh

# Exponer puerto
EXPOSE 8000

# Comando para iniciar el servidor con SSE
CMD ["./start-server.sh"]