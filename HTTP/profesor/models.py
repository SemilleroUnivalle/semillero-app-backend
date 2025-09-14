from django.db import models
from django.conf import settings
from modulo.models import Modulo

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    celular = models.CharField(max_length=15, blank=True, null=True)
    contrasena = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=20, unique=True)
    area_desempeño = models.CharField(max_length=100, blank=True, null=True)
    grado_escolaridad = models.CharField(max_length=100, blank=True, null=True)
    modulo = models.ForeignKey(Modulo, on_delete=models.SET_NULL, related_name='profesores', null=True, blank=True)
    
    def __str__(self):
        return (
            f"ID: {self.id_profesor} | "
            f"Usuario: {self.user} | "
            f"Nombre: {self.nombre} {self.apellido} | "
            f"Correo: {self.email} | "
            f"Teléfono: {self.celular} | "
            f"Documento: {self.numero_documento} | "
            
            
        )
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ['id_profesor']
