#!/bin/bash
set -e  # Detener el script si hay un error

echo "Instalando dependencias antes del despliegue..."
sudo apt update -y
sudo apt install -y python3-full python3-pip python3-venv software-properties-common

# Agregar PPA de Python si no está presente
if ! grep -q "deadsnakes" /etc/apt/sources.list /etc/apt/sources.list.d/*; then
    echo "Agregando repositorio de Python 3.10..."
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
fi

# Verificar si Python 3.10 está instalado, si no, instalarlo
if ! python3.10 --version &>/dev/null; then
    echo "Instalando Python 3.10..."
    sudo apt install -y python3.10 python3.10-venv python3.10-full python3.10-dev
fi

# Cambiar Python 3 predeterminado a 3.10
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Crear carpeta si no existe
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

source venv/bin/activate

# Instalar dependencias dentro del entorno virtual
pip install --upgrade pip
pip install -r requirements.txt

echo "Before install completado."
