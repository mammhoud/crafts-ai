# ruff: noqa: E402
"""django_seed.providers — shim pointing to craftsai.seeder.providers."""
import warnings

warnings.warn(
    "django_seed.providers is deprecated. Use craftsai.seeder.providers instead.",
    DeprecationWarning,
    stacklevel=2,
)
from craftsai.seeder.providers import *  # noqa: F401, F403
