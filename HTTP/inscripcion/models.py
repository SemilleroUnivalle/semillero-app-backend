from django.db import models
from estudiante.models import Estudiante
from modulo.models import Modulo
from oferta_categoria.models import OfertaCategoria
from oferta_academica.models import OfertaAcademica
from grupo.models import Grupo
from auditlog.registry import auditlog
from auditlog.models import LogEntry

def recibo_pago_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    numero_documento = instance.id_estudiante.numero_documento
    return f'recibos_pago/{numero_documento}.{ext}'

def constancia_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    numero_documento = instance.id_estudiante.numero_documento
    return f'constancias/{numero_documento}.{ext}'

def certificado_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    numero_documento = instance.id_estudiante.numero_documento
    return f'certificados/{numero_documento}.{ext}'

class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    id_modulo = models.ForeignKey(Modulo, on_delete=models.SET_NULL, null=True)
    id_oferta_categoria = models.ForeignKey(OfertaCategoria, on_delete=models.SET_NULL, null=True)
    oferta_academica = models.ForeignKey(OfertaAcademica, on_delete=models.SET_NULL, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    tipo_vinculacion = models.CharField(max_length=255)
    terminos = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    
    recibo_pago = models.FileField(
        upload_to=recibo_pago_upload_to, null=True, blank=True,
        help_text="Sube un documento pdf del recibo de pago"
    )

    constancia = models.FileField(
        upload_to=constancia_upload_to, null=True, blank=True,
        help_text="Sube un documento pdf de la constancia de estudio"
    )

    certificado = models.FileField(
        upload_to=certificado_upload_to, null=True, blank=True,
        help_text="Sube un documento pdf del certificado de funcionario"
    )

    #verificacion de documentos
    verificacion_recibo_pago = models.BooleanField(default=False)
    verificacion_constancia = models.BooleanField(default=False)
    verificacion_certificado = models.BooleanField(default=False)
    estado = models.CharField(max_length=12,default='No revisado')
    #id de la auditoria que corresponde a cada cambio solo en el caso de:
        # - Foto
        # - Documento de identidad
        # - Informacion
    audit_documento_recibo_pago = models.OneToOneField(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="inscripcion_recibo_pago",
        null=True,
        blank=True
    )
    audit_constancia = models.OneToOneField(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="inscripcion_constancia",
        null=True,
        blank=True
    )
    audit_certificado = models.OneToOneField(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="inscripcion_certificado",
        null=True,
        blank=True
    )


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

auditlog.register(Inscripcion)
