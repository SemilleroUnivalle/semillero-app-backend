from django.db import models

class Acudiente(models.Model):
    id_acudiente = models.AutoField(primary_key=True)
    nombre_acudiente = models.CharField(max_length=100)
    tipo_documento_acudiente = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=50)
    celular_acudiente = models.CharField(max_length=50)
    direccion_acudiente = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.numero_celular}"
