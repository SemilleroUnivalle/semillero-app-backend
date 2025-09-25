from django.db import models
from django.conf import settings
from modulo.models import Modulo
from usuario.models import Usuario


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
