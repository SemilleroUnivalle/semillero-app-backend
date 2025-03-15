#!/bin/bash
echo "Iniciando aplicación en EC2..."
cd /home/ubuntu/app
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
