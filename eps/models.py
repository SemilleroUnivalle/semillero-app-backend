from django.db import models

class EPS(models.Model):
    """
    Modelo para la tabla EPS.
    """
    id_eps = models.AutoField(primary_key=True)
    nombre_eps = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.id_eps}-{self.nombre_eps}'
    
    class Meta:
        verbose_name = 'EPS'
        verbose_name_plural = 'EPS'
        ordering = ['nombre_eps']
