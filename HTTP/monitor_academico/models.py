from django.db import models
from django.conf import settings
from modulo.models import Modulo
from usuario.models import Usuario


def d10_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'd10_monitor_academico/{instance.numero_documento}.{ext}'
def tabulado_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'tabulado_monitor_academico/{instance.numero_documento}.{ext}'
def estado_mat_financiera_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return f'estado_mat_financiera_monitor_academico/{instance.numero_documento}.{ext}'

class MonitorAcademico(Usuario):
    semestre = models.CharField(max_length=100, blank=True, null=True)
    area_desempeño = models.CharField(max_length=50)
    modulo = models.ForeignKey(Modulo, on_delete=models.SET_NULL, related_name='monitor_academico', null=True, blank=True)
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
        verbose_name = "MonitorAcademico"
        verbose_name_plural = "MonitoresAcademicos"
        ordering = ['id']
