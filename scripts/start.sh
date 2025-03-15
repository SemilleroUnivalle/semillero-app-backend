#!/bin/bash
source /home/ubuntu/app/venv/bin/activate
cd /home/ubuntu/app
nohup gunicorn --workers 3 --bind 0.0.0.0:8000 myproject.wsgi:application &
