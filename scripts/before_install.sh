#!/bin/bash
echo "Instalando dependencias antes del despliegue..."
sudo apt update -y
sudo apt install -y python3-pip python3-venv
cd /home/ubuntu/app
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
