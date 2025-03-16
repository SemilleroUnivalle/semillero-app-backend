#!/bin/bash
set -e  # Detiene el script si hay un error

echo "📦 Creando entorno virtual..."
cd app/
python3 -m venv venv

echo "📦 Activando entorno virtual..."
source venv/bin/activate

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ Instalación completada."