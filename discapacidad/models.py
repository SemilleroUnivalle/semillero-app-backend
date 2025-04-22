from django.db import models

class Discapacidad(models.Model):
    id_discapacidad = models.AutoField(primary_key=True)
    tipo_discapacidad = models.CharField(max_length=50, unique=True)
    info_discapacidad = models.TextField()
    
    class Meta:
        db_table = 'discapacidad'
        verbose_name = 'Discapacidad'
        verbose_name_plural = 'Discapacidades'

    def __str__(self):
        return self.nombre
