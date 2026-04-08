import warnings

warnings.warn(
    "django_seed.providers is deprecated. Use django_rseal.seeder.providers instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.seeder.providers import *  # noqa: F401, F403
