"""django_seed.orchestrator — shim pointing to craftsai.orchestrator."""
import warnings

warnings.warn(
    "django_seed.orchestrator is deprecated. Use craftsai.orchestrator instead.",
    DeprecationWarning,
    stacklevel=2,
)
from craftsai.orchestrator import *  # noqa: F401, F403, E402
