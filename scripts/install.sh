#!/bin/bash
cd /home/ubuntu/app
sudo python3 -m venv venv
source venv/bin/activate
sudo chown -R ubuntu:ubuntu venv/
pip install -r requirements.txt
