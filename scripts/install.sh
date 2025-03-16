#!/bin/bash
set -e  # Detener el script si hay un error

# Definir ruta del entorno virtual
VENV_PATH="/home/ubuntu/app/venv"

# Crear el entorno virtual si no existe
if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
fi

# Activar el entorno virtual
source "$VENV_PATH/bin/activate"

# Actualizar pip dentro del entorno virtual
pip install --upgrade pip

# Instalar dependencias desde requirements.txt
pip install -r /home/ubuntu/app/requirements.txt

echo "Instalación completada exitosamente."
