import warnings

warnings.warn(
    "django_seed.services is deprecated. Use django_rseal.services instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.services import *  # noqa: F401, F403
