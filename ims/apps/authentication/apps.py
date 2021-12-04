from django.apps import AppConfig
from .settings import CUSER_SETTINGS


class AuthenticationConfig(AppConfig):
    name = 'authentication'
    verbose_name = CUSER_SETTINGS['app_verbose_name']

    def ready(self):
        import authentication.signals