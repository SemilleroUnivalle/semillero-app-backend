from django.db import models
from django.conf import settings
from usuario.models import Usuario
from auditlog.registry import auditlog
from auditlog.models import LogEntry

def d10_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'd10_monitor_administrativo/{instance.numero_documento}.{ext}'
def tabulado_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'tabulado_monitor_administrativo/{instance.numero_documento}.{ext}'
def estado_mat_financiera_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'estado_mat_financiera_monitor_administrativo/{instance.numero_documento}.{ext}'

class MonitorAdministrativo(Usuario):
    d10_pdf = models.FileField(
        upload_to=d10_upload_to, null=True, blank=True,
    )
    tabulado_pdf = models.FileField(
        upload_to=tabulado_upload_to, null=True, blank=True,
    )
    estado_mat_financiera_pdf = models.FileField(
        upload_to=estado_mat_financiera_upload_to, null=True, blank=True,
    )

    verificacion_d10 = models.BooleanField(default=False)
    verificacion_tabulado = models.BooleanField(default=False)
    verificacion_estado_mat_financiera = models.BooleanField(default=False)
    verificacion_documento_identidad = models.BooleanField(default=False)
    verificacion_rut = models.BooleanField(default=False)
    verificacion_certificado_bancario = models.BooleanField(default=False)

    audit_d10 = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="monitor_administrativo_d10",
        null=True,
        blank=True
    )
    audit_tabulado = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="monitor_administrativo_tabulado",
        null=True,
        blank=True
    )
    audit_estado_mat_financiera = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="monitor_administrativo_estado_mat_financiera",
        null=True,
        blank=True
    )
    audit_documento_identidad = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="monitor_administrativo_documento_identidad",
        null=True,
        blank=True
    )
    audit_rut = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="monitor_administrativo_rut",
        null=True,
        blank=True
    )
    audit_certificado_bancario = models.ForeignKey(
        LogEntry,
        on_delete=models.CASCADE,
        related_name="monitor_administrativo_certificado_bancario",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "MonitorAdministrativo"
        verbose_name_plural = "MonitoresAdministrativos"
        ordering = ['id']

auditlog.register(MonitorAdministrativo)