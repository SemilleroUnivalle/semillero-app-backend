from django.db import models
from django.conf import settings

def documento_identidad_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'documentos_identidad_usuario/{instance.numero_documento}.{ext}'

def rut_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'rut_usuario/{instance.numero_documento}.{ext}'

def certificado_bancario_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'certificado_bancario_usuario/{instance.numero_documento}.{ext}'

class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Para definir el tipo de usuario
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=128, blank=True)  
    numero_documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100)
    is_active = models.BooleanField(default=True)
    ciudad_residencia = models.CharField(max_length=100)
    eps = models.CharField(max_length=100) # Entidad promotora de salud
    tipo_documento = models.CharField(max_length=20) # Tipo de documento de identidad
    genero = models.CharField(max_length=10) # Género del estudiante
    fecha_nacimiento = models.DateField() # Fecha de nacimiento del estudiante
    telefono_fijo = models.CharField(max_length=15) # Teléfono del estudiante
    celular = models.CharField(max_length=15) # Celular del estudiante
    departamento_residencia = models.CharField(max_length=50) # Departamento de residencia del estudiante
    comuna_residencia = models.CharField(max_length=10) # Comuna de residencia del estudiante
    direccion_residencia = models.CharField(max_length=255) # Dirección de residencia del estudiante
    documento_identidad_pdf = models.FileField(
        upload_to=documento_identidad_upload_to, null=True, blank=True,
    )
    rut_pdf = models.FileField(
        upload_to=rut_upload_to, null=True, blank=True,
    )
    certificado_bancario_pdf = models.FileField(
        upload_to=certificado_bancario_upload_to, null=True, blank=True,
    )