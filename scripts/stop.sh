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

echo "🧹 Limpiando archivos temporales..."

# Limpiar archivos de caché
if [ -d ~/.cache ]; then
    du -sh ~/.cache
    read -p "¿Deseas limpiar el directorio de caché? (s/n): " confirm_cache
    if [ "$confirm_cache" = "s" ] || [ "$confirm_cache" = "S" ]; then
        rm -rf ~/.cache/*
        echo "✅ Caché limpiada exitosamente."
    fi
fi

# Listar archivos ocultos que podrían no ser necesarios
echo "📋 Archivos temporales que podrían eliminarse:"
find ~ -maxdepth 1 -type f -name ".*_history" -o -name ".lesshst" -o -name ".viminfo"

echo "✅ Limpieza completada."