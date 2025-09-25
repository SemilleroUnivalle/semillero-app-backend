from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import MonitorAdministrativo
from rest_framework.authtoken.models import Token
import threading

@receiver(pre_delete, sender=MonitorAdministrativo)
def delete_user_when_admin_deleted(sender, instance, **kwargs):
    """Elimina tokens y usuario cuando se elimina un administrador"""
    pdf_fields = [
        'documento_identidad_pdf',
        'rut_pdf',
        'certificado_bancario_pdf',
        'd10_pdf',
        'tabulado_pdf',
        'estado_mat_financiera_pdf',
    ]

    def delete_pdf(pdf_file):
        if pdf_file:
            try:
                pdf_file.delete(save=False)
            except Exception:
                pass

    threads = []
    for field in pdf_fields:
        pdf_file = getattr(instance, field, None)
        if pdf_file:
            t = threading.Thread(target=delete_pdf, args=(pdf_file,))
            t.start()
            threads.append(t)

    # Espera a que todas las eliminaciones de archivos terminen
    for t in threads:
        t.join()

    try:
        user = instance.user
        # Elimina tokens primero
        Token.objects.filter(user=user).delete()
        # Luego elimina el usuario
        user.delete()
    except Exception:
        pass