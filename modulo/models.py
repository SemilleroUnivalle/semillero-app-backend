from django.db import models

class Modulo(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    id_area = models.ForeignKey('area.Area', on_delete=models.CASCADE)
    nombre_modulo = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_modulo
