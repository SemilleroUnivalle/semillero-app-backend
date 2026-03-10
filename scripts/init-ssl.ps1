# 1. Cargar variables desde el .env
if (Test-Path .env) {
    Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object {
        $parts = $_.Split('=', 2)
        if ($parts.Count -eq 2) {
            $name = $parts[0].Trim()
            $value = $parts[1].Trim()
            Set-Item "env:$name" $value
        }
    }
}
else {
    Write-Error "Archivo .env no encontrado."
    exit
}

# Validar DOMINIO
$DOMINIO = $env:DOMINIO
if (-not $DOMINIO) {
    Write-Error "La variable DOMINIO no está definida en el .env"
    exit
}

Write-Host "--- Iniciando proceso SSL para: $DOMINIO ---" -ForegroundColor Cyan

# 2. Definir ruta de certificados
$data_path = "./certbot/conf"

if (Test-Path "$data_path/live/$DOMINIO") {
    Write-Host "Ya existen certificados para $DOMINIO. Saltando creación de dummy." -ForegroundColor Yellow
}
else {
    Write-Host "--- Creando certificados dummy (temporales) ---" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path "$data_path/live/$DOMINIO"
    
    docker compose run --rm --entrypoint "sh -c 'openssl req -x509 -nodes -newkey rsa:2048 -days 1 -keyout /etc/letsencrypt/live/$DOMINIO/privkey.pem -out /etc/letsencrypt/live/$DOMINIO/fullchain.pem -subj ''/CN=localhost'''" certbot
}

Write-Host "--- Iniciando Nginx ---" -ForegroundColor Cyan
docker compose up -d nginx

Write-Host "--- Solicitando certificados reales a Let's Encrypt ---" -ForegroundColor Cyan
$EMAIL = if ($env:EMAIL_HOST_USER) { $env:EMAIL_HOST_USER } else { "johan.tombe@correounivalle.edu.co" }

docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email "$EMAIL" --agree-tos --no-eff-email -d "$DOMINIO"

Write-Host "--- Recargando Nginx con los certificados reales ---" -ForegroundColor Cyan
docker compose exec nginx nginx -s reload

Write-Host "¡Listo! Tu sitio ya debería tener HTTPS activo para $DOMINIO." -ForegroundColor Green
