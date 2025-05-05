from django.db import models
from categoria.models import Categoria
from oferta_academica.models import OfertaAcademica

class OfertaCategoria(models.Model):
    
    id_oferta_categoria = models.AutoField(primary_key=True)
    id_oferta_academica = models.ForeignKey(
        OfertaAcademica,
        on_delete=models.CASCADE,
        related_name='oferta_categoria'
    )
    id_categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE,
        related_name='oferta_categoria',
    )
    precio_publico = models.DecimalField(max_digits=10, decimal_places=2)
    precio_privado = models.DecimalField(max_digits=10, decimal_places=2)
    precio_univalle = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_finalizacion = models.DateField()
    
    def __str__(self):
        return (
            f"ID: {self.id_oferta_categoria} | "
            f"Oferta Académica: {self.id_oferta_academica} | "
            f"Categoría: {self.id_categoria} | "
            f"Precio Público: {self.precio_publico} | "
            f"Precio Privado: {self.precio_privado} | "
            f"Precio Univalle: {self.precio_univalle} | "
            f"Fecha Finalización: {self.fecha_finalizacion}"
        )
    
    class Meta:
        verbose_name = 'Oferta Categoria'
        verbose_name_plural = 'Ofertas Categoria'
        ordering = ['id_oferta_categoria']