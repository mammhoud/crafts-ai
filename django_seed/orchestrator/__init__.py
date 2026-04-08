import warnings

warnings.warn(
    "django_seed.orchestrator is deprecated. Use django_rseal.workflows.orchestrator instead.",
    DeprecationWarning,
    stacklevel=2,
)
from django_rseal.workflows.orchestrator import *  # noqa: F401, F403
