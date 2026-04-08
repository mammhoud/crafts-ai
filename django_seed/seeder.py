# ruff: noqa: E402
"""django_seed.seeder — shim pointing to craftsai.seeder."""
import warnings

warnings.warn(
    "django_seed.seeder is deprecated. Use craftsai.seeder instead.",
    DeprecationWarning,
    stacklevel=2,
)
from craftsai.seeder import *  # noqa: F401, F403
