from django.db import models
from profesor.models import Profesor
from monitor_academico.models import MonitorAcademico

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True)
    monitor_academico = models.ForeignKey(MonitorAcademico, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
