from django.db import models

class GradoEscolar(models.Model):
    """Modelo de grado escolar"""
    id_grado = models.AutoField(primary_key=True)
    nombre_grado = models.CharField(max_length=50, unique=True)
    

    def __str__(self):
        return self.nombre_grado
