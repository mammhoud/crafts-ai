import warnings

warnings.warn(
    "django_seed.management.commands.invite_user is deprecated. "
    "Use django_rseal.management.commands.invite_user instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.management.commands.invite_user import Command  # noqa: F401
