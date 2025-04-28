from django.db import models
from oferta_categoria.models import OfertaCategoria

class Modulo(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    id_area = models.ForeignKey('area.Area', on_delete=models.CASCADE)
    id_oferta_categoria = models.ForeignKey(OfertaCategoria, on_delete=models.PROTECT, related_name='modulo', blank=True, null=True)
    nombre_modulo = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.id_modulo, self.nombre_modulo
