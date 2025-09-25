from django.db import models
from django.conf import settings
from usuario.models import Usuario

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

    class Meta:
        verbose_name = "MonitorAdministrativo"
        verbose_name_plural = "MonitoresAdministrativos"
        ordering = ['id']