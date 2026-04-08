import warnings

warnings.warn(
    "django_seed.management.commands.send_invitations_from_csv is deprecated. "
    "Use django_rseal.management.commands.send_invitations_from_csv instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.management.commands.send_invitations_from_csv import Command  # noqa: F401
