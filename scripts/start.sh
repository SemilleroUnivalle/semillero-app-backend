#!/bin/bash

echo "🚀 Iniciando Gunicorn..."

# Activar entorno virtual
source /home/ubuntu/app/venv/bin/activate

# Moverse al directorio de la aplicación
cd /home/ubuntu/app

# Iniciar Gunicorn con logs
gunicorn --config gunicorn_config.py semillero_backend.wsgi:application

echo "✅ Gunicorn iniciado correctamente."