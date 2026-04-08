import warnings

warnings.warn(
    "django_seed.seeder is deprecated. Use django_rseal.seeder.seeder instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.seeder.seeder import *  # noqa: F401, F403
