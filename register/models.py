from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator
from curse.models import Modulo
from django.conf import settings 
#Modelo para el registro de estudiantes
class Estudiante(models.Model):

    GeneroOpciones = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ]
    TipoIdentificacionOpciones = [
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('OT', 'Otro')
    ]
    EstamentoOpciones = [('Publico', 'Público'), ('Privado', 'Privado')]
    
    # Relación con el usuario de Django
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='estudiante',
        null=True,
        blank=True
    )

    # Información del estudiante
    Foto = models.ImageField(upload_to='estudiantes/fotos/', validators=[FileExtensionValidator(['jpg', 'jpeg'])], null=True, blank=True)
    Nombre = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100)
    TipoIdentificacion = models.CharField(max_length=2, choices=TipoIdentificacionOpciones, null=True, blank=True)
    NumeroIdentificacion = models.CharField(max_length=20, unique=True)
    CiudadNacimiento = models.CharField(max_length=100, null=True, blank=True)
    CorreoElectronico = models.EmailField(default='default@default.com')
    ConfirmacionCorreo = models.EmailField(null=True, blank=True)
    NumeroCelular = models.CharField(max_length=15, null=True, blank=True)
    NumeroTelefonoAlternativo = models.CharField(max_length=15, null=True, blank=True)
    Genero = models.CharField(max_length=1, choices=GeneroOpciones, null=True, blank=True)
    FechaNacimiento = models.DateField(null=True, blank=True)
    DepartamentoResidencia = models.CharField(max_length=100, null=True, blank=True)
    CiudadResidencia = models.CharField(max_length=100, null=True, blank=True)
    DireccionResidencia = models.CharField(max_length=200, null=True, blank=True)
    EntidadSalud = models.CharField(max_length=100, null=True, blank=True)
    NombreColegio = models.CharField(max_length=100, null=True, blank=True)
    EstamentoColegio = models.CharField(max_length=10, choices=EstamentoOpciones, null=True, blank=True)
    GradoEscolaridad = models.CharField(max_length=50, null=True, blank=True)
    ModuloMatricular = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name="Inscripciones", null=True, blank=True)
    
    # Información del acudiente
    NombreAcudiente = models.CharField(max_length=100, null=True, blank=True)
    NumeroCelularAcudiente = models.CharField(max_length=15, null=True, blank=True)

    # Información sobre discapacidad
    TieneDiscapacidad = models.BooleanField(null=True, blank=True)
    TipoDiscapacidad = models.CharField(max_length=100, blank=True, null=True)
    DescripcionDiscapacidad = models.TextField(blank=True, null=True)

    # Información de pago
    TipoVinculacionOpciones = [('Particular', 'Particular'), ('Univalle', 'Relación Univalle')]
    TipoVinculacion = models.CharField(max_length=15, choices=TipoVinculacionOpciones, null=True, blank=True)
    ValorConsignado = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    NumeroRecibo = models.CharField(max_length=50, null=True, blank=True)
    FechaConsignacion = models.DateField(null=True, blank=True)
    NombreResponsablePago = models.CharField(max_length=100, null=True, blank=True)
    TipoIdentificacionResponsablePago = models.CharField(max_length=2, choices=TipoIdentificacionOpciones, null=True, blank=True)
    NumeroIdentificacionResponsablePago = models.CharField(max_length=20, null=True, blank=True)
    DireccionResidenciaResponsablePago = models.CharField(max_length=200, null=True, blank=True)
    NumeroCelularResponsablePago = models.CharField(max_length=15, null=True, blank=True)
    CorreoElectronicoResponsablePago = models.EmailField(null=True, blank=True)

    # Documentos adjuntos
    DocumentoIdentidad = models.FileField(upload_to='estudiantes/documentos/', validators=[FileExtensionValidator(['pdf'])], null=True, blank=True)
    ReciboPago = models.FileField(upload_to='estudiantes/documentos/', validators=[FileExtensionValidator(['pdf'])], null=True, blank=True)
    ConstanciaEstudio = models.FileField(upload_to='estudiantes/documentos/', validators=[FileExtensionValidator(['pdf'])], blank=True, null=True)
    
    password = models.CharField(max_length=128, default='1111')
    is_profile_complete = models.BooleanField(default=False)