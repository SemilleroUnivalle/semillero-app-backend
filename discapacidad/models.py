from django.db import models

class Discapacidad(models.Model):
    id_discapacidad = models.AutoField(primary_key=True)
    tipo_discapacidad = models.CharField(max_length=50, unique=True)
    info_discapacidad = models.TextField()
    
    class Meta:
        verbose_name = 'Discapacidad'
        verbose_name_plural = 'Discapacidades'
        ordering = ['id_discapacidad']

    def __str__(self):
        return f'{self.id_discapacidad} - {self.tipo_discapacidad} - {self.info_discapacidad}'
