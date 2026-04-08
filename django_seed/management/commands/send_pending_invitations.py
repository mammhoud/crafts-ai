import warnings

warnings.warn(
    "django_seed.management.commands.send_pending_invitations is deprecated. "
    "Use django_rseal.management.commands.send_pending_invitations instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.management.commands.send_pending_invitations import Command  # noqa: F401
