from django.db import models
from acudiente.models import Acudiente
from django.conf import settings

def documento_identidad_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'documentos_identidad/{instance.numero_documento}.{ext}'

def foto_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'fotos/{instance.numero_documento}.{ext}'

class Estudiante(models.Model):
    """Modelo de usuario para estudiantes"""
    #Campos obligatorios
    id_estudiante = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=128,blank=True)  
    numero_documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100)
    is_active = models.BooleanField(default=True)
    #Relacion uno a uno acudiente
    acudiente = models.ForeignKey(
        Acudiente,
        on_delete=models.CASCADE,
        related_name='estudiante',
        null=False,
        blank=False,
    )
    ciudad_residencia = models.CharField(max_length=100)
    eps = models.CharField(max_length=100) #Entidad promotora de salud
    grado = models.CharField(max_length=20) #Grado al que pertenece el estudiante
    colegio = models.CharField(max_length=100, default='N/A') #Colegio al que pertenece el estudiante
    tipo_documento = models.CharField(max_length=20) #Tipo de documento de identidad
    genero = models.CharField(max_length=10) #Género del estudiante
    fecha_nacimiento = models.DateField() #Fecha de nacimiento del estudiante
    telefono_fijo = models.CharField(max_length=15) #Teléfono del estudiante
    celular = models.CharField(max_length=15) #Celular del estudiante
    departamento_residencia = models.CharField(max_length=50) #Departamento de residencia del estudiante
    comuna_residencia = models.CharField(max_length=10) #Comuna de residencia del estudiante
    direccion_residencia = models.CharField(max_length=255) #Dirección de residencia del estudiante
    estamento = models.CharField(max_length=50) #Estamento al que pertenece el estudiante
    discapacidad = models.BooleanField(default=False) #Indica si el estudiante tiene alguna discapacidad
    tipo_discapacidad = models.CharField(max_length=50, default='Ninguna') #Tipo de discapacidad del estudiante
    descripcion_discapacidad = models.TextField(max_length=100, default='Ninguna') #Descripción de la discapacidad del estudiante
    area_desempeño = models.CharField(max_length=100, blank=True, null=True) #En el caso de los profesores que van para formacion docente
    grado_escolaridad = models.CharField(max_length=100, blank=True, null=True) #En el caso de los profesores que van para formacion docente

    documento_identidad = models.FileField(
        upload_to=documento_identidad_upload_to, null=True, blank=True,
        help_text="Sube un documento pdf del documento de identidad del estudiante"
    )
    foto = models.ImageField(
        upload_to=foto_upload_to, null=True, blank=True,
        help_text="Sube una imagen del estudiante"
    )
    
    def __str__(self):
        acudiente_info = f"Acudiente: {self.acudiente}" if self.acudiente else "Sin acudiente"
        return (
            f"ID: {self.id_estudiante} | Usuario: {self.user} | "
            f"Nombre: {self.nombre} {self.apellido} | Doc: {self.tipo_documento} {self.numero_documento} | "
            f"Email: {self.email} | Activo: {self.is_active} |"
            f"{acudiente_info} | Ciudad res.: {self.ciudad_residencia} |"
            f"EPS: {self.eps} | Grado: {self.grado} | Género: {self.genero} | "
            f"Fecha nac.: {self.fecha_nacimiento} | Tel. fijo: {self.telefono_fijo} | "
            f"Celular: {self.celular} | Dpto. res.: {self.departamento_residencia} | "
            f"Comuna: {self.comuna_residencia} | Dirección: {self.direccion_residencia} | "
            f"Estamento: {self.estamento} | Discapacidad: {self.discapacidad} | "
            f"Tipo discapacidad: {self.tipo_discapacidad}"
        )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['id_estudiante']

