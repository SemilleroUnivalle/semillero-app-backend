from django.db import models

class Acudiente(models.Model):
    id_acudiente = models.AutoField(primary_key=True)
    nombre_acudiente = models.CharField(max_length=100)
    apellido_acudiente = models.CharField(max_length=100)
    tipo_documento_acudiente = models.CharField(max_length=20, unique=True)
    numero_documento_acudiente = models.CharField(max_length=20)
    email_acudiente = models.EmailField(max_length=100, unique=True)
    celular_acudiente = models.CharField(max_length=20)

    def __str__(self):
        return f"ID: {self.id_acudiente} | Nombre: {self.nombre_acudiente} | Documento: {self.tipo_documento_acudiente} {self.numero_documento} | Celular: {self.celular_acudiente} | Dirección: {self.direccion_acudiente}"
    
    class Meta:
        verbose_name = "Acudiente"
        verbose_name_plural = "Acudientes"
        ordering = ['id_acudiente']
