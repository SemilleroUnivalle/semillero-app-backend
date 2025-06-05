#!/bin/bash
# Limpiar archivos pyc y carpetas __pycache__ de despliegues anteriores
find /home/ubuntu/app -name '*.pyc' -delete
find /home/ubuntu/app -type d -name '__pycache__' -exec rm -rf {} +

# Actualizar e instalar dependencias
sudo apt update -y
sudo apt install -y python3-pip python3-venv
