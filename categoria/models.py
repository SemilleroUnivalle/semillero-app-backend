from django.db import models

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.id_categoria} - {self.nombre} - {"Activo" if self.estado else "Inactivo"}'
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id_categoria']
