from django.db import models

class HistorialCambios(models.Model):
    id_cambio = models.AutoField(primary_key=True)
    id_inscripcion = models.IntegerField()
    tipo_cambio = models.CharField(max_length=50)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    motivo_cambio = models.TextField()
    id_nueva_inscripcion = models.IntegerField()
    id_modulo_nuevo = models.IntegerField()
    id_periodo_aplazado = models.IntegerField()
    
    class Meta:
        db_table = 'historial_cambios'
        verbose_name = 'Historial de Cambios'
        verbose_name_plural = 'Historial de Cambios'
