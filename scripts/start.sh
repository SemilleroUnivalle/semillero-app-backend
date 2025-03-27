#!/bin/bash
cd /home/ec2-user/api
source venv/bin/activate
# Cambia esto si usás Django, Flask, etc.
# Ejemplo Django:
nohup python manage.py runserver 0.0.0.0:8000 &
