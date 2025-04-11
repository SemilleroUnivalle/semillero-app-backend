from django.db import models

class EPS(models.Model):
    """
    Modelo para la tabla EPS.
    """
    id_eps = models.AutoField(primary_key=True)
    nombre_eps = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
