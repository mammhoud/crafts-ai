import warnings

warnings.warn(
    "django_seed.tasks is deprecated. Use django_rseal.tasks.django_q instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.tasks.django_q import *  # noqa: F401, F403
