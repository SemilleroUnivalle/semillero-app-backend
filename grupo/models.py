from django.db import models

class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=100)

    def __str__(self):
        return f'ID: {self.id_grupo} | Grupo: {self.nombre_grupo} | Oferta Módulo: {self.id_oferta_modulo}'
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        ordering = ['id_grupo']
