# 🚀 Solución Rápida: Error "Unable to locate credentials"

## ❌ Problema
```
ERROR creando registro 1 (numero_documento=300): Unable to locate credentials
```

## ✅ Solución Inmediata (Almacenamiento Local)

### Paso 1: Copia el archivo de ejemplo
```bash
cp .env.example .env
```

### Paso 2: Edita el archivo `.env` y asegúrate que tenga:
```bash
USE_S3=False
```

### Paso 3: Reinicia el contenedor
```bash
docker-compose down
docker-compose up -d
```

### Paso 4: Ejecuta el script de carga
```bash
docker exec semillero_backend python -m fixtures.carga_mon_academico
```

---

## 📝 Explicación

- **Antes**: El sistema intentaba subir archivos a AWS S3 pero no encontraba credenciales
- **Ahora**: Con `USE_S3=False`, los archivos se guardan localmente en `HTTP/media/`
- **Producción**: Cuando despliegues, cambia a `USE_S3=True` y agrega las credenciales de AWS

---

## 🔐 Para Usar S3 (Producción)

Si necesitas usar S3, edita `.env`:

```bash
USE_S3=True
AWS_ACCESS_KEY_ID=tu_access_key_aqui
AWS_SECRET_ACCESS_KEY=tu_secret_key_aqui
AWS_STORAGE_BUCKET_NAME=archivos-estudiantes
AWS_S3_REGION_NAME=us-east-1
```

---

## ✅ Verificar Configuración

Dentro del contenedor:
```bash
docker exec -it semillero_backend bash
python manage.py shell
```

En el shell de Python:
```python
from django.conf import settings
print(f"USE_S3: {settings.USE_S3}")
print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'S3')}")
```

Deberías ver:
```
✅ Usando almacenamiento local (desarrollo)
USE_S3: False
MEDIA_ROOT: /app/media
```
