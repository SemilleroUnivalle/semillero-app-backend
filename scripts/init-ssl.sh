#!/bin/bash

# 1. Cargar variables desde el .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: Archivo .env no encontrado."
    exit 1
fi

# Validar que la variable DOMINIO existe
if [ -z "$DOMINIO" ]; then
    echo "Error: La variable DOMINIO no está definida en el .env"
    exit 1
fi

echo "--- Iniciando proceso SSL para: $DOMINIO ---"

# 2. Definir ruta de certificados
data_path="./certbot/conf"

if [ -d "$data_path/live/$DOMINIO" ]; then
    echo "Ya existen certificados para $DOMINIO. Saltando creación de certificados dummy."
else
    echo "--- Creando certificados dummy (temporales) ---"
    mkdir -p "$data_path/live/$DOMINIO"
    
    # Usamos docker-compose para generar los archivos dummy con openssl
    docker-compose run --rm --entrypoint \
      "openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
      -keyout /etc/letsencrypt/live/$DOMINIO/privkey.pem \
      -out /etc/letsencrypt/live/$DOMINIO/fullchain.pem \
      -subj '/CN=localhost'" nginx
fi

echo "--- Iniciando Nginx ---"
# Levantamos el servicio nginx. Al usar /etc/nginx/templates/, 
# Nginx generará automáticamente /etc/nginx/conf.d/default.conf procesando las variables.
docker-compose up -d nginx

echo "--- Solicitando certificados reales a Let's Encrypt ---"
# Se usa el email configurado en el .env o uno por defecto
EMAIL=${EMAIL_HOST_USER:-"johan.tombe@correounivalle.edu.co"}

docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos --no-eff-email \
    -d "$DOMINIO"

echo "--- Recargando Nginx con los certificados reales ---"
docker-compose exec nginx nginx -s reload

echo "¡Listo! Tu sitio ya debería tener HTTPS activo para $DOMINIO."
