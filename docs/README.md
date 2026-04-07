# Django-seed Documentation

This directory contains documentation for the django-seed library - a Django database seeding library with email automation capabilities.

## Contents

This documentation directory will contain:

### Core Features
- Database seeding and test data generation
- Email automation system
- Role-based access control
- Background task processing

### Components (To be added)
- `models.md` - EmailLog, UserRole, UserGroup models
- `services.md` - Email service, invitation service, queue manager
- `tasks.md` - Background tasks and periodic jobs
- `templates.md` - Email template system
- `management.md` - Management commands (invite_user, send_pending_invitations)
- `usage.md` - Usage examples and best practices
- `api.md` - API reference

## What is django-seed?

django-seed is a Django library that provides:
- Database seeding with test data generation
- Email automation system with role-based access control
- Background task processing with Django Q
- Email logging and audit trail
- Invitation services for user onboarding
- Periodic task scheduling

## Installation

```bash
# Install from GitHub
pip install git+https://github.com/mammhoud/django-seed.git@main

# Or with uv
uv add "django-seed @ git+https://github.com/mammhoud/django-seed.git@main"
```

## Quick Start

```python
# Database seeding
from django_seed import Seed

seeder = Seed.seeder()
seeder.add_entity(MyModel, 10)
seeder.execute()

# Email automation
from django_seed.services import EmailService

email_service = EmailService()
email_service.send_invitation(
    recipient='user@example.com',
    template_name='emails/invitation.html',
    context={'name': 'John Doe'}
)
```

## Configuration

Add to your Django settings:

```python
INSTALLED_APPS = [
    ...
    'django_seed',
    'django_q',  # For background tasks
]

# Django Q configuration
Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 4,
    'timeout': 300,
    'retry': 3600,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
}

# Email automation
REPORT_EMAIL_FROM = 'noreply@example.com'
REPORT_EMAIL_TO = 'admin@example.com'
```

## Contributing

When adding new documentation:
1. Place it in this directory
2. Add an entry to this README
3. Include code examples
4. Document parameters and return values
5. Add usage examples

## Related Documentation

- Main README: [../README.md](../README.md)
- GitHub Repository: https://github.com/mammhoud/django-seed
