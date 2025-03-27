#!/bin/bash
echo "Iniciando script de parada..."
echo "Intentando detener procesos de manage.py..."

# Intentar matar el proceso
pkill -f manage.py
RESULT=$?

# Reportar resultado
if [ $RESULT -eq 0 ]; then
    echo "Proceso(s) detenido(s) exitosamente."
elif [ $RESULT -eq 1 ]; then
    echo "No se encontraron procesos para detener. Continuando normalmente."
else
    echo "Error al intentar detener procesos: $RESULT"
fi

# Siempre salir con éxito
echo "Script de parada completado."
exit 0