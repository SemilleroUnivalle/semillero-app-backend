from django.db import models
from estudiante.models import Estudiante
from modulo.models import Modulo

class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    id_modulo = models.ForeignKey(Modulo, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('R', 'Rechazado'),
    ], default='A')
    grupo = models.CharField(max_length=255, default='Grupo 0')
    fecha_inscripcion = models.DateField(auto_now_add=True)
    tipo_vinculacion = models.CharField(max_length=255)
    terminos = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return (
            f"ID: {self.id_inscripcion} | "
            f"Estudiante: {self.id_estudiante} | "
            f"Módulo: {self.id_modulo} | "
            f"Grupo: {self.grupo} | "
            f"Fecha: {self.fecha_inscripcion} | "
            f"Tipo Vinculacion: {self.tipo_vinculacion} | "
            f"Términos aceptados: {self.terminos}"
        )
    
    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        ordering = ['fecha_inscripcion']
