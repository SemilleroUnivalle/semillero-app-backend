#!/bin/bash
set -e  # Detiene el script si hay un error

echo "Instalando dependencias antes del despliegue..."
sudo apt update -y
sudo apt install -y python3-full python3-pip python3-venv

# Verificar si Python 3.10 está instalado y configurarlo como predeterminado
if python3 --version | grep -q "Python 3.12"; then
    echo "Cambiando a Python 3.10..."
    sudo apt install -y python3.10 python3.10-venv python3.10-full python3.10-dev
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
fi

# Crear carpeta si no existe
mkdir -p /home/ubuntu/app

cd /home/ubuntu/app

# Crear entorno virtual si no existew
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

source venv/bin/activate

# Instalar dependencias dentro del entorno virtual
pip install --upgrade pip --break-system-packages
pip install -r requirements.txt

echo "Before install completado."
