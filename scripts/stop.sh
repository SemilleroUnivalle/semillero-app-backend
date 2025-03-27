#!/bin/bash
echo "Stopping old process (if running)..."

# Mata el proceso solo si existe
pkill -f gunicorn || echo "No process found"

echo "Process stopped successfully!"
exit 0  # Asegura que CodeDeploy no falle
