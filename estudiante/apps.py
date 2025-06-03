from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estudiante'
    
    def ready(self):
        import estudiante.signals
