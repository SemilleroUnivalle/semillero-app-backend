from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Estudiante
from rest_framework.authtoken.models import Token

@receiver(pre_delete, sender=Estudiante)
def delete_user_when_estudiante_deleted(sender, instance, **kwargs):
    """Elimina tokens y usuario cuando se elimina un estudiante"""
    try:
        user = instance.user
        # Elimina tokens primero
        Token.objects.filter(user=user).delete()
        # Luego elimina el usuario
        user.delete()
    except Exception:
        # Si no hay usuario o tokens, simplemente continúa
        pass