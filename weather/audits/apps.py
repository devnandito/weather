from django.apps import AppConfig


class AuditAppConfig(AppConfig):
    """Audits app config"""

    name = 'weather.audits'
    verbose_name = 'Audits'

    def ready(self):
        import weather.audits.signals