from django.db import models
from inscripcion.models import Inscripcion

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha_asistencia = models.DateField()
    estado_asistencia = models.CharField(max_length=20, choices=[
        ('P', 'Presente'),
        ('A', 'Ausente'),
        ('T', 'Tarde'),
    ], default='P')
    comentarios = models.TextField(max_length=500, default='Ninguno')
    
    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['fecha_asistencia']

    def __str__(self):
        return f'Asistencia {self.id_asistencia} - {self.id_inscripcion} - {self.fecha_asistencia} - {self.estado_asistencia} - {self.comentarios}'
