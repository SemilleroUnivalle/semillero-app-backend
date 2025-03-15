#!/bin/bash
echo "Instalando dependencias antes del despliegue..."
sudo apt update -y
sudo apt install -y python3-pip python3-venv

# Navegar al directorio de la aplicación
cd /home/ubuntu/app

# Crear el entorno virtual solo si no existe
if [ ! -d "venv" ]; then
    echo "Creando el entorno virtual..."
    python3 -m venv venv
else
    echo "El entorno virtual ya existe. Activándolo..."
fi

# Activar el entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt