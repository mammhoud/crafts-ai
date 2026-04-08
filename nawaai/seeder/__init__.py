"""Faker-based data seeder — framework-agnostic."""
import warnings

warnings.warn(
    "nawaai.seeder re-exports from django_rseal.seeder. "
    "For standalone use without Django, use Faker directly.",
    UserWarning,
    stacklevel=2,
)
