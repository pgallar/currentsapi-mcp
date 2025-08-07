#!/bin/bash

# Verificar variables de entorno requeridas
required_vars=(
    "CURRENTS_API_KEY"
)

# Cargar variables de entorno desde .env si existe
if [ -f ".env" ]; then
    source .env
    echo "✅ Variables de entorno cargadas desde .env"
fi

missing_vars=0
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Missing required environment variable: $var"
        missing_vars=$((missing_vars + 1))
    else
        echo "✅ Found environment variable: $var"
    fi
done

# Verificar directorios necesarios
required_dirs=(
    "src"
    "logs"
)

missing_dirs=0
for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ Missing required directory: $dir"
        missing_dirs=$((missing_dirs + 1))
    else
        echo "✅ Found directory: $dir"
    fi
done

# Verificar archivos necesarios
required_files=(
    "requirements.txt"
    "healthcheck.sh"
    "src/main.py"
)

missing_files=0
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        missing_files=$((missing_files + 1))
    else
        echo "✅ Found file: $file"
    fi
done

# Verificar permisos de ejecución
if [ ! -x "healthcheck.sh" ]; then
    echo "❌ healthcheck.sh is not executable"
    chmod +x healthcheck.sh
    echo "✅ Fixed permissions for healthcheck.sh"
fi

if [ ! -x "check-env.sh" ]; then
    chmod +x check-env.sh
fi

# Resumen
echo -e "\n=== Environment Check Summary ==="
echo "Missing variables: $missing_vars"
echo "Missing directories: $missing_dirs"
echo "Missing files: $missing_files"

if [ $missing_vars -gt 0 ] || [ $missing_dirs -gt 0 ] || [ $missing_files -gt 0 ]; then
    echo -e "\n❌ Please fix the issues above before starting the server"
    exit 1
else
    echo -e "\n✅ All checks passed! You can start the server"
    exit 0
fi