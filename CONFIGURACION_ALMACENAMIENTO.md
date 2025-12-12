# ========================================
# CONFIGURACIÓN: Almacenamiento Local vs S3
# ========================================

## Problema Actual
El error "Unable to locate credentials" ocurre porque boto3 (AWS SDK) no encuentra las credenciales de AWS.

## Soluciones

### ✅ Opción 1: Usar Almacenamiento Local (Recomendado para Desarrollo)

Modifica `settings.py` para usar almacenamiento local en desarrollo:

```python
# En settings.py, reemplaza la sección STORAGES por:

import os

USE_S3 = os.getenv('USE_S3', 'False') == 'True'

if USE_S3:
    # Configuración S3 (Producción)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'archivos-estudiantes')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_DEFAULT_ACL = 'private'
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = 'virtual'
    
    STORAGES = {
        "default": {
            "BACKEND": "semillero_backend.storage_backends.MediaStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
else:
    # Configuración Local (Desarrollo)
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
```

Luego en tu `.env`:
```bash
USE_S3=False  # Para desarrollo local
# USE_S3=True  # Para producción con S3
```

---

### ✅ Opción 2: Configurar Credenciales de AWS

#### Paso 1: Obtener Credenciales de AWS

1. Ve a AWS Console: https://console.aws.amazon.com/
2. Navega a **IAM** > **Users** > Tu usuario
3. Ve a **Security Credentials**
4. Crea un **Access Key** (si no tienes uno)
5. Descarga y guarda:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

#### Paso 2: Crear Archivo `.env`

Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_STORAGE_BUCKET_NAME=archivos-estudiantes
AWS_S3_REGION_NAME=us-east-1

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

#### Paso 3: Compartir Credenciales de Forma Segura

**⚠️ NUNCA subas el archivo `.env` a Git**

Para compartir con otro PC:
1. Envía el archivo `.env` por un canal seguro (email encriptado, password manager, etc.)
2. O comparte las credenciales verbalmente/por mensaje privado
3. La otra persona crea su propio archivo `.env` con esas credenciales

---

### ✅ Opción 3: Variables de Entorno en Docker

Si usas Docker, agrega las variables al `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_STORAGE_BUCKET_NAME=archivos-estudiantes
      - AWS_S3_REGION_NAME=us-east-1
```

Y asegúrate de que el archivo `.env` esté en la misma carpeta que `docker-compose.yml`.

---

## Recomendación

Para **desarrollo local**, usa **Opción 1** (almacenamiento local).
Para **producción**, usa **Opción 2** (S3 con credenciales).

---

## Verificar Configuración

Después de configurar, verifica dentro del contenedor:

```bash
docker exec semillero_backend python manage.py shell
```

Luego en el shell de Python:
```python
from django.conf import settings
print(f"USE_S3: {getattr(settings, 'USE_S3', 'Not defined')}")
print(f"AWS_ACCESS_KEY_ID: {settings.AWS_ACCESS_KEY_ID[:10]}..." if settings.AWS_ACCESS_KEY_ID else "Not configured")
print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'Not defined')}")
```
