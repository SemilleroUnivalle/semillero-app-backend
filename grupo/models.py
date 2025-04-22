from django.db import models

class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=100)
    id_oferta_modulo = models.ForeignKey('oferta_modulo.OfertaModulo', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
