#!/bin/bash
set -e  # Detener el script si hay un error

echo "Iniciando aplicación en EC2..."

cd /home/ubuntu/app || exit

# Activar entorno virtual
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: No se encontró el entorno virtual. Abortando."
    exit 1
fi

# Verificar si Gunicorn está instalado
if ! which gunicorn &>/dev/null; then
    echo "Gunicorn no está instalado. Instalándolo..."
    pip install gunicorn
fi

# Aplicar migraciones
python manage.py migrate --noinput

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Reiniciar Gunicorn si ya estaba corriendo, o iniciarlo si no
if sudo systemctl is-active --quiet gunicorn; then
    echo "Reiniciando Gunicorn..."
    sudo systemctl restart gunicorn
else
    echo "Iniciando Gunicorn..."
    sudo systemctl start gunicorn
fi

echo "Aplicación iniciada correctamente."
