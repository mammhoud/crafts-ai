import warnings

warnings.warn(
    "django_seed.management.commands.seed is deprecated. "
    "Use django_rseal.management.commands.seed instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.management.commands.seed import Command  # noqa: F401
