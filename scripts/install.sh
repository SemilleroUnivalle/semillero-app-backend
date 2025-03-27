#!/bin/bash
cd /home/ubuntu/api/
sudo apt install -y python3.12-venv python3-pip 
if [ ! -d "/home/ubuntu/api/venv" ]; then
    python3 -m venv /home/ubuntu/api/venv
fi

# Activa el entorno virtual
source /home/ubuntu/api/venv/bin/activate

# Actualiza pip y setuptools dentro del entorno virtual
pip install --upgrade pip setuptools

# Instala dependencias del proyecto
pip install -r /home/ubuntu/api/requirements.txt

# Desactiva el entorno virtual
deactivate
