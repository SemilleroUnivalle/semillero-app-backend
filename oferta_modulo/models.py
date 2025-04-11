from django.db import models

class OfertaModulo(models.Model):
    id_oferta = models.AutoField(primary_key=True)
    id_modulo = models.ForeignKey('modulo.Modulo', on_delete=models.CASCADE)
    id_periodo_academico = models.ForeignKey('periodo_academico.PeriodoAcademico', on_delete=models.CASCADE)
    precio_publico = models.DecimalField(max_digits=10, decimal_places=2)
    precio_privado = models.DecimalField(max_digits=10, decimal_places=2)
    precio_relacion_univalente = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'oferta_modulo'
        verbose_name = 'Oferta Modulo'
        verbose_name_plural = 'Ofertas Modulos'
