from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('administrador', 'Administrador'),
        ('monitor_academico', 'Monitor_academico'),
        ('monitor_administrativo', 'Monitor_administrativo'),
    )
    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES, default='estudiante')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'