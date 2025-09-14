from django.db import models

class SeguimientoAcademico(models.Model):
    id_seguimiento = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey('inscripcion.Inscripcion', on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField()

    def __str__(self):
        return (
            f"ID: {self.id_seguimiento} | Inscripción: {self.id_inscripcion} | Fecha: {self.fecha} | "
            f"Descripción: {self.descripcion} | Calificación: {self.calificacion} | "
            f"Observaciones: {self.observaciones}"
        )
    class Meta:
        verbose_name = 'Seguimiento Academico'
        verbose_name_plural = 'Seguimientos Academicos'
        ordering = ['fecha']
