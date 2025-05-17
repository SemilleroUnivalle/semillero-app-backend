FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Puerto en el que se ejecuta Gunicorn
EXPOSE 8080

# Comando para ejecutar al iniciar el contenedor
CMD ["sh", "-c", "python manage.py migrate && gunicorn -c gunicorn_config.py semillero_backend.wsgi:application"]