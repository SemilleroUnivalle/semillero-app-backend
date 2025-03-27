#!/bin/bash
# Detener el proceso anterior (si está corriendo)

# Verificar si el proceso está en ejecución antes de intentar terminarlo
if pgrep -f manage.py > /dev/null; then
    echo "Deteniendo proceso manage.py existente..."
    pkill -f manage.py
    echo "Proceso detenido correctamente."
else
    echo "No se encontró proceso manage.py en ejecución."
fi

# Asegurar que el script siempre termine con éxito
exit 0