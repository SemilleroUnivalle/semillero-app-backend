from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Administrador
from rest_framework.authtoken.models import Token

@receiver(pre_delete, sender=Administrador)
def delete_user_when_admin_deleted(sender, instance, **kwargs):
    """Elimina tokens y usuario cuando se elimina un administrador"""
    try:
        user = instance.user
        # Elimina tokens primero
        Token.objects.filter(user=user).delete()
        # Luego elimina el usuario
        user.delete()
    except Exception:
        # Si no hay usuario o tokens, simplemente continúa
        pass