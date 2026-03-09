#!/bin/bash
cd /home/ubuntu/app
bash scripts/init-ssl.sh
docker-compose up -d --build