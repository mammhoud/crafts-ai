import warnings

warnings.warn(
    "django_seed.models is deprecated. Use django_rseal.email.models instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.email.models import *  # noqa: F401, F403
