from django.db import models
from acudiente.models import Acudiente

class Estudiante(models.Model):
    """Modelo de usuario para estudiantes"""
    #Campos obligatorios
    id_estudiante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    #Relacion uno a uno acudiente
    acudiente = models.OneToOneField(
        Acudiente,
        on_delete=models.CASCADE,
        related_name='estudiante',
        null=True,
        blank=True
    )
    # Nuevos campos
    registro_fase = models.PositiveSmallIntegerField(default=1)  # 1 = Fase inicial, 2 = Fase completada

    # Campos opcionales para la segunda fase del registro
    ciudad_residencia = models.CharField(max_length=100, blank=True, null=True)
    ciudad_documento = models.CharField(max_length=100, blank=True, null=True) #La ciudad donde se expidió el documento de identidad
    id_eps = models.CharField(max_length=20, blank=True, null=True) #Entidad prestadora de salud a la que pertenece el estudiante
    id_grado = models.CharField(max_length=20, blank=True, null=True) #Grado al que pertenece el estudiante
    tipo_documento = models.CharField(max_length=20, blank=True, null=True) #Tipo de documento de identidad
    genero = models.CharField(max_length=10, blank=True, null=True) #Género del estudiante
    fecha_nacimiento = models.DateField(blank=True, null=True) #Fecha de nacimiento del estudiante
    telefono_fijo = models.CharField(max_length=15, blank=True, null=True) #Teléfono del estudiante
    celular = models.CharField(max_length=15, blank=True, null=True) #Celular del estudiante
    departamento_residencia = models.CharField(max_length=100, blank=True, null=True) #Departamento de residencia del estudiante
    comuna_residencia = models.CharField(max_length=100, blank=True, null=True) #Comuna de residencia del estudiante
    direccion_residencia = models.CharField(max_length=255, blank=True, null=True) #Dirección de residencia del estudiante
    estamento = models.CharField(max_length=50, blank=True, null=True) #Estamento al que pertenece el estudiante
    discapacidad = models.BooleanField(default=False) #Indica si el estudiante tiene alguna discapacidad
    tipo_discapacidad = models.CharField(max_length=50, blank=True, null=True) #Tipo de discapacidad del estudiante
    descripcion_discapacidad = models.TextField(blank=True, null=True) #Descripción de la discapacidad del estudiante

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.numero_documento})"

