from django.db import models

class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_area = models.CharField(max_length=100, unique=True)
    estado_area = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['id_area']

    def __str__(self):
        return f"ID: {self.id_area} | Nombre: {self.nombre_area} | Descripción: {self.descripcion_area} | Estado: {'Activo' if self.estado_area else 'Inactivo'}"
