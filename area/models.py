from django.db import models

class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_area = models.CharField(max_length=100, unique=True)
    descripcion_area = models.TextField(blank=True, null=True)
    estado_area = models.BooleanField(blank=True, default=True)
    
    class Meta:
        db_table = 'area'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return self.nombre
