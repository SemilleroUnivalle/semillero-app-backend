from django.apps import AppConfig


class ProfesorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profesor'
    
    def ready(self):
        import profesor.signals
