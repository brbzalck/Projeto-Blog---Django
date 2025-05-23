from django.apps import AppConfig


class SiteSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_setup'

    def ready(self):
        import site_setup.signals