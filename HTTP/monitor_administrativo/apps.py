from django.apps import AppConfig


class MonitorAdministrativoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitor_administrativo'

    def ready(self):
        import monitor_administrativo.signals
