import warnings

warnings.warn(
    "django_seed.guessers is deprecated. Use django_rseal.seeder.guessers instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.seeder.guessers import *  # noqa: F401, F403
