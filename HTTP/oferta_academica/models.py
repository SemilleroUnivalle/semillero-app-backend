from django.db import models

class OfertaAcademica(models.Model):
    ESTADOS_OFERTA = [
        ('inscripcion', 'En Inscripciones'),
        ('desarrollo', 'En Desarrollo'),
        ('finalizado', 'Finalizado'),
    ]

    id_oferta_academica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField(help_text="Fecha de inicio de las inscripciones")
    fecha_desarrollo = models.DateField(null=True, blank=True, help_text="Fecha de inicio de las clases/desarrollo")
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_OFERTA,
        default='inscripcion'
    )

    def __str__(self):
        return f"Oferta: {self.nombre} | Estado: {self.get_estado_display()} | Inicio: {self.fecha_inicio}"

    class Meta:
        verbose_name = "Oferta Académica"
        verbose_name_plural = "Ofertas Académicas"
        ordering = ['-fecha_inicio']
