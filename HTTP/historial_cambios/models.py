from django.db import models

class HistorialCambios(models.Model):
    id_cambio = models.AutoField(primary_key=True)
    id_inscripcion = models.IntegerField()
    tipo_cambio = models.CharField(max_length=50)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    motivo_cambio = models.TextField(max_length=500)
    id_nueva_inscripcion = models.IntegerField()
    id_modulo_nuevo = models.IntegerField()
    id_periodo_aplazado = models.IntegerField()
    Observaciones = models.TextField(max_length=500, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Historial de Cambios'
        verbose_name_plural = 'Historial de Cambios'
        ordering = ['fecha_cambio']

    def __str__(self):
        return (
            f"ID Cambio: {self.id_cambio} | "
            f"ID Inscripción: {self.id_inscripcion} | "
            f"Tipo Cambio: {self.tipo_cambio} | "
            f"Fecha Cambio: {self.fecha_cambio} | "
            f"Motivo: {self.motivo_cambio} | "
            f"Nueva Inscripción: {self.id_nueva_inscripcion} | "
            f"Módulo Nuevo: {self.id_modulo_nuevo} | "
            f"Periodo Aplazado: {self.id_periodo_aplazado}"
        )
