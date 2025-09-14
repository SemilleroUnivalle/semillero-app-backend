from django.db import models
from inscripcion.models import Inscripcion

class EvaluacionPrograma(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    nota_metodologia = models.DecimalField(max_digits=5, decimal_places=2)
    nota_estudiante = models.DecimalField(max_digits=5, decimal_places=2)
    nota_profesor = models.DecimalField(max_digits=5, decimal_places=2)
    nota_monitor = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField(max_length=500, default='Ninguna')
    
    class Meta:
        verbose_name = 'Evaluacion Programa'
        verbose_name_plural = 'Evaluaciones Programas'
        ordering = ['fecha']

    def __str__(self):
        return (
            f"ID: {self.id_evaluacion} | Inscripción: {self.id_inscripcion} | Fecha: {self.fecha} | "
            f"Nota metodología: {self.nota_metodologia} | Nota estudiante: {self.nota_estudiante} | "
            f"Nota profesor: {self.nota_profesor} | Nota monitor: {self.nota_monitor} | "
            f"Observaciones: {self.observaciones}"
        )
