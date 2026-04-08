import warnings

warnings.warn(
    "django_seed.logging_config is deprecated. Use django_rseal.logging_config instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.logging_config import *  # noqa: F401, F403
