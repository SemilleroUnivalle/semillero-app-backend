#!/bin/bash
set -e  # Detiene el script si hay un error

echo "🔥 Limpiando archivos de implementaciones anteriores..."

echo "📦 Actualizando paquetes y dependencias..."
sudo apt update -y
sudo apt install -y python3-pip python3-venv

echo "✅ Preparación completada."

