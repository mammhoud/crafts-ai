"""
Django app configuration for django_seed.
"""

from django.apps import AppConfig


class DjangoSeedConfig(AppConfig):
    """Configuration for the django_seed application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_seed'
    verbose_name = 'Django Seed - Email Automation'

    def ready(self):
        """
        Perform initialization when the app is ready.
        This is called once Django has loaded all apps.
        """
        pass
