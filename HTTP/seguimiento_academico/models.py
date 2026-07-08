from django.db import models
from decimal import Decimal

class SeguimientoAcademico(models.Model):
    id_seguimiento = models.AutoField(primary_key=True)
    id_inscripcion = models.OneToOneField('inscripcion.Inscripcion', on_delete=models.CASCADE, related_name='seguimiento')
    
    # Notas requeridas
    seguimiento_1 = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    seguimiento_2 = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    nota_conceptual_docente = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    nota_conceptual_estudiante = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    fecha_ultimo_cambio = models.DateTimeField(auto_now=True)
    observaciones = models.TextField(blank=True, null=True)

    @property
    def nota_final(self):
        """Calcula una nota final sugerida (opcional, ajusta los pesos)"""
        # Ejemplo: 30% Seg1, 30% Seg2, 20% Concept Docente, 20% Estudiante
        return (self.seguimiento_1 * Decimal('0.3') + 
                self.seguimiento_2 * Decimal('0.3') + 
                self.nota_conceptual_docente * Decimal('0.2') + 
                self.nota_conceptual_estudiante * Decimal('0.2'))

    def __str__(self):
        return f"Seguimiento {self.id_inscripcion.id_estudiante.nombre} - Insc: {self.id_inscripcion_id}"

    class Meta:
        verbose_name = 'Seguimiento Académico'
        verbose_name_plural = 'Seguimientos Académicos'
