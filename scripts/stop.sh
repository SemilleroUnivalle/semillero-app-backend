#!/bin/bash

echo "🛑 Deteniendo Gunicorn..."

# Buscar si Gunicorn está corriendo
if pgrep -f gunicorn > /dev/null
then
    pkill -f gunicorn
    echo "✅ Gunicorn detenido exitosamente."
else
    echo "⚠️ No se encontró ningún proceso de Gunicorn en ejecución."
fi
