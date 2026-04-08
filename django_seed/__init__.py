"""
django_seed — DEPRECATED.

This package is deprecated. Use:
- craftsai for standalone AI/MCP/seeding (no Django)
- django_rseal for Django-integrated automation
"""
import warnings

warnings.warn(
    "django_seed is deprecated. Use 'craftsai' for standalone AI/MCP "
    "or 'django_rseal' for Django automation.",
    DeprecationWarning,
    stacklevel=2,
)
