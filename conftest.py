"""
Pytest configuration for django-seed tests.
Configures Django settings for test execution.
"""

import django
from django.conf import settings


def pytest_configure(config):
    """Configure Django settings for tests."""
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'django_seed',
            ],
            DEFAULT_FROM_EMAIL='noreply@example.com',
            EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
            SECRET_KEY='test-secret-key-for-django-seed-tests',
            USE_TZ=True,
            SITE_URL='http://localhost:8000',
            TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [],
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.request',
                        ],
                    },
                }
            ],
        )
        django.setup()
