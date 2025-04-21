from django.db import models

class OfertaAcademica(models.Model):
    id_oferta_academica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()

    def __str__(self):
        return self.nombre
