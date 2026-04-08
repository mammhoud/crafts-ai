"""django_seed app config — minimal shim."""
from django.apps import AppConfig


class DjangoSeedConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_seed"
    verbose_name = "Django Seed (deprecated)"
