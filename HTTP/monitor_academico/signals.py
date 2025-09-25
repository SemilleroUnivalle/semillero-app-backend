from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import MonitorAcademico
from rest_framework.authtoken.models import Token

@receiver(pre_delete, sender=MonitorAcademico)
def delete_user_when_professor_deleted(sender, instance, **kwargs):
    """Elimina tokens y usuario cuando se elimina un Monitor"""
    pdf_fields = [
        'documento_identidad_pdf',
        'rut_pdf',
        'certificado_bancario_pdf',
        'd10_pdf',
        'tabulado_pdf',
        'estado_mat_financiera_pdf',
    ]

    # Elimina todos los archivos PDF de S3 si existen
    for field in pdf_fields:
        pdf_file = getattr(instance, field, None)
        if pdf_file:
            try:
                pdf_file.delete(save=False)
            except Exception:
                pass

    try:
        user = instance.user
        # Elimina tokens primero
        Token.objects.filter(user=user).delete()
        # Luego elimina el usuario
        user.delete()
    except Exception:
        # Si no hay usuario o tokens, simplemente continúa
        pass