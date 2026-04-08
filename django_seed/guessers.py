# ruff: noqa: E402
"""django_seed.guessers — shim pointing to craftsai.seeder.guessers."""
import warnings

warnings.warn(
    "django_seed.guessers is deprecated. Use craftsai.seeder.guessers instead.",
    DeprecationWarning,
    stacklevel=2,
)
from craftsai.seeder.guessers import *  # noqa: F401, F403
