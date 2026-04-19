# Changelog

All notable changes to nawaai are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-04-15

### Changed

#### Pure Python Boundary Enforcement (Phase 5)
- Audited all modules for Django imports using `scripts/check_boundaries.py` (`nawaai-no-django` rule)
- Removed all Django imports found during audit — replaced with dependency injection or pure Python alternatives
- Re-verified: zero Django, Wagtail, Celery, or project-specific imports anywhere in this package

#### Naming Conventions (Phase 8)
- All module files use `snake_case`
- All classes use `PascalCase`
- All functions and variables use `snake_case`

### Boundary Guarantees
- `scripts/check_boundaries.py` reports zero violations for the `nawaai-no-django` rule
- Safe to use in any Python project without Django installed
- No runtime dependencies on any web framework

## [1.x.x] - Prior releases

See git history for changes prior to the 2.0.0 architectural refactoring.
