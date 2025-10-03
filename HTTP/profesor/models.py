from django.db import models
from django.conf import settings
from modulo.models import Modulo
from usuario.models import Usuario
from auditlog.registry import auditlog
from auditlog.models import LogEntry


def hoja_vida_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'hoja_vida_profesor/{instance.numero_documento}.{ext}'
def certificado_laboral_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'certificado_laboral_profesor/{instance.numero_documento}.{ext}'
def certificado_academico_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'certificado_academico_profesor/{instance.numero_documento}.{ext}'

class Profesor(Usuario):
    area_desempeño = models.CharField(max_length=50)
    grado_escolaridad = models.CharField(max_length=50)
    modulo = models.ForeignKey(Modulo, on_delete=models.SET_NULL, related_name='profesores', null=True, blank=True)
    hoja_vida_pdf = models.FileField(
        upload_to=hoja_vida_upload_to, null=True, blank=True,
    )
    certificado_laboral_pdf = models.FileField(
        upload_to=certificado_laboral_upload_to, null=True, blank=True,
    )
    certificado_academico_pdf = models.FileField(
        upload_to=certificado_academico_upload_to, null=True, blank=True,
    )

    verificacion_hoja_vida = models.BooleanField(default=False)
    verificacion_certificado_laboral = models.BooleanField(default=False)
    verificacion_certificado_academico = models.BooleanField(default=False)
    verificacion_documento_identidad = models.BooleanField(default=False)
    verificacion_rut = models.BooleanField(default=False)
    verificacion_certificado_bancario = models.BooleanField(default=False)

    audit_hoja_vida = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="profesor_d10",
        null=True,
        blank=True
    )
    audit_certificado_laboral = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="profesor_tabulado",
        null=True,
        blank=True
    )
    audit_certificado_academico = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="profesor_estado_mat_financiera",
        null=True,
        blank=True
    )
    audit_documento_identidad = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="profesor_documento_identidad",
        null=True,
        blank=True
    )
    audit_rut = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="profesor_rut",
        null=True,
        blank=True
    )
    audit_certificado_bancario = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="profesor_certificado_bancario",
        null=True,
        blank=True
    )

    
    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"Usuario: {self.user} | "
            f"Nombre: {self.nombre} {self.apellido} | "
            f"Correo: {self.email} | "
            f"Teléfono: {self.celular} | "
            f"Documento: {self.numero_documento} | "
            
            
        )
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ['id']

auditlog.register(Profesor)