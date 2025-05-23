from django.db import models
from django.conf import settings

class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=20, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"ID: {self.id_administrador} | Usuario: {self.user} | Nombre: {self.nombre} {self.apellido} | Correo: {self.correo} | Documento: {self.numero_documento} | Creado: {self.fecha_creacion} | Modificado: {self.fecha_modificacion}"
    
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        ordering = ['id_administrador']