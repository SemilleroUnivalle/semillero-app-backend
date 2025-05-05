from django.db import models

class GradoEscolar(models.Model):
    """Modelo de grado escolar"""
    id_grado = models.AutoField(primary_key=True)
    nombre_grado = models.CharField(max_length=50, unique=True)
    

    def __str__(self):
        return f'ID: {self.id_grado} | Grado: {self.nombre_grado}'
    class Meta:
        verbose_name = "Grado Escolar"
        verbose_name_plural = "Grados Escolares"
        ordering = ['id_grado']
