#!/bin/bash

# Script para iniciar el servidor MCP de News con SSE

echo "=== Iniciando Servidor MCP de News con SSE ==="
echo ""

# Cargar variables de entorno si existe el archivo .env
if [ -f ".env" ]; then
    source .env
    echo "✅ Variables de entorno cargadas desde .env"
else
    echo "ℹ️ Archivo .env no encontrado, usando variables de entorno del sistema"
fi

# Verificar entorno
./check-env.sh
if [ $? -ne 0 ]; then
    echo "❌ Error en la verificación del entorno"
    exit 1
fi

# Verificar API key
if [ -z "$CURRENTS_API_KEY" ]; then
    echo "❌ CURRENTS_API_KEY no está configurada"
    exit 1
fi

echo "✅ API key configurada"
echo ""

# Configurar variables de entorno para SSE
export HOST=0.0.0.0
export PORT=8000
export USE_SSE=true
export RELOAD=true

echo "🔧 Configuración SSE:"
echo "   - Transport: SSE"
echo "   - Host: $HOST"
echo "   - Port: $PORT"
echo ""

# Iniciar el servidor con configuración SSE
echo "Iniciando servidor MCP con SSE..."
echo ""

python -m src.main

echo ""
echo "=== Servidor MCP detenido ==="