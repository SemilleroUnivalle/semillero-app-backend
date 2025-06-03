from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    user = reset_password_token.user
    reset_url = f"https://recuperacion-contrasena-semillero.vercel.app/?token={reset_password_token.key}"
    
    subject = "SEMILLERO - Restablecimiento de contraseña"
    from_email = "no-reply@tudominio.com"
    to_email = [user.email]
    
    # Renderiza la plantilla HTML
    html_content = render_to_string(
        "login/password_reset_email.html",
        {"user": user, "reset_url": reset_url}
    )
    # Mensaje en texto plano (fallback)
    text_content = f"Hola {user.first_name}!\n\nUsa este enlace para restablecer tu contraseña: {reset_url}\n\nSi no solicitaste este cambio, ignora este mensaje."
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()