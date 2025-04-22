from django.db import models

class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey('estudiante.Estudiante', on_delete=models.CASCADE)
    id_oferta_modulo = models.ForeignKey('oferta_modulo.OfertaModulo', on_delete=models.CASCADE)
    id_grupo = models.ForeignKey('grupo.Grupo', on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    convenio = models.CharField(max_length=255)
    terminos = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
