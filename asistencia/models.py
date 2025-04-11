from django.db import models

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey('inscripcion.Inscripcion', on_delete=models.CASCADE)
    fecha_asistencia = models.DateField()
    estado_asistencia = models.CharField(max_length=20, choices=[
        ('P', 'Presente'),
        ('A', 'Ausente'),
        ('T', 'Tarde'),
    ], default='P')
    comentarios = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return f"{self.id_participante} - {self.fecha_asistencia}"
