from django.db import models

class OfertaAcademica(models.Model):
    id_oferta_academica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')

    def __str__(self):
        return f"Oferta Académica {self.id_oferta_academica} - Nombre: {self.nombre} - Fecha Inicio: {self.fecha_inicio} - Estado: {self.estado}"
    class Meta:
        verbose_name = "Oferta Académica"
        verbose_name_plural = "Ofertas Académicas"
        ordering = ['fecha_inicio']
