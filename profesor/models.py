from django.db import models
from django.conf import settings

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    contrasena = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_contratacion = models.DateField(blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
