#!/bin/bash

echo "🚀 Iniciando Gunicorn..."

# Activar entorno virtual
source /home/ubuntu/app/venv/bin/activate

# Moverse al directorio de la aplicación
cd /home/ubuntu/app

# Iniciar Gunicorn con logs
gunicorn --bind 0.0.0.0:8000 project_semillero.wsgi:application

echo "✅ Gunicorn iniciado correctamente."