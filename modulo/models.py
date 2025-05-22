from django.db import models
from oferta_categoria.models import OfertaCategoria
from categoria.models import Categoria
from area.models import Area

class Modulo(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    id_oferta_categoria = models.ManyToManyField(
    OfertaCategoria, 
    related_name='modulo',
    blank=True)
    id_categoria = models.ForeignKey(
    Categoria, 
    on_delete=models.SET_NULL,
    related_name='modulo_categoria',
    null=True)
    id_area = models.ForeignKey(Area, on_delete=models.SET_NULL, related_name='modulo',null=True)

    nombre_modulo = models.CharField(max_length=100, unique=True)
    descripcion_modulo = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"ID: {self.id_modulo} | "
            f"Nombre: {self.nombre_modulo} | "
            f"Categoría: {self.id_categoria} | "
            f"Oferta Categoría: {self.id_oferta_categoria} | "
            f"Área: {self.id_area} | "
            f"Descripción: {self.descripcion_modulo} | "
            f"Activo: {self.estado}"
        )
    
    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'
        ordering = ['id_modulo']
