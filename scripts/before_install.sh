#!/bin/bash
set -e  # Detiene el script si hay un error

echo "🔥 Limpiando archivos de implementaciones anteriores..."

# Crear la carpeta app si no existe
sudo mkdir -p /home/ubuntu/app

# Eliminar versiones anteriores de la aplicación
sudo rm -rf /home/ubuntu/app/*
sudo rm -rf /home/ubuntu/app/venv
sudo rm -rf /opt/codedeploy-agent/deployment-root/*

# Limpiar caché de paquetes pip
rm -rf /home/ubuntu/.cache/pip
rm -rf /tmp/*

# Limpiar logs antiguos
sudo truncate -s 0 /var/log/aws/codedeploy-agent.log

echo "📦 Actualizando paquetes y dependencias..."
sudo apt update -y
sudo apt install -y python3-pip python3-venv

echo "✅ Preparación completada."

