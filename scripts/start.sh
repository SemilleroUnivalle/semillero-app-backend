#!/bin/bash

echo "🚀 Iniciando Gunicorn..."

# Activar entorno virtual
source /home/ubuntu/app/venv/bin/activate

# Moverse al directorio de la aplicación
cd /home/ubuntu/app

# Iniciar Gunicorn con logs
nohup gunicorn --workers 3 --bind 0.0.0.0:8000 semillero_backend.wsgi:application > /home/ubuntu/app/gunicorn.log 2>&1 &

echo "✅ Gunicorn iniciado correctamente."