from django.db import models

class EvaluacionPrograma(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey('inscripcion.Inscripcion', on_delete=models.CASCADE)
    fecha = models.DateField()
    nota_metodologia = models.DecimalField(max_digits=5, decimal_places=2)
    nota_estudiante = models.DecimalField(max_digits=5, decimal_places=2)
    nota_profesor = models.DecimalField(max_digits=5, decimal_places=2)
    nota_monitor = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField()
    
    class Meta:
        db_table = 'evaluacion_programa'
        verbose_name = 'Evaluacion Programa'
        verbose_name_plural = 'Evaluaciones Programas'

    def __str__(self):
        return self.nombre
