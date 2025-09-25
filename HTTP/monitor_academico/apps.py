from django.apps import AppConfig


class MonitorAcademicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitor_academico'

    def ready(self):
        import monitor_academico.signals
