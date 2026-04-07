"""
settings_example.py
-------------------
Example Django settings snippets for integrating django-seed email automation.

Copy the relevant sections into your project's settings.py and adjust values
to match your environment. All sensitive values should come from environment
variables (see .env.example).
"""

import os

# ---------------------------------------------------------------------------
# Django Q Configuration
# ---------------------------------------------------------------------------
# Add 'django_q' to INSTALLED_APPS:
#
#   INSTALLED_APPS = [
#       ...
#       'django_q',
#       'django_seed',
#   ]

Q_CLUSTER = {
    # Cluster name - used to identify this cluster in the Django Q admin
    'name': 'django_seed_cluster',

    # Number of worker processes to spawn
    'workers': int(os.environ.get('DJANGO_Q_WORKERS', 4)),

    # Maximum number of tasks a worker will process before recycling
    'recycle': 500,

    # Task timeout in seconds (5 minutes)
    'timeout': 300,

    # Retry failed tasks after this many seconds
    'retry': 60,

    # Maximum number of retries for a failed task
    'max_attempts': 3,

    # Compress task payloads to save memory
    'compress': True,

    # Save successful task results to the database
    'save_limit': 250,

    # Redis broker configuration
    'redis': {
        'host': os.environ.get('DJANGO_Q_REDIS_HOST', 'localhost'),
        'port': int(os.environ.get('DJANGO_Q_REDIS_PORT', 6379)),
        'db': 0,
        # Uncomment if Redis requires a password:
        # 'password': os.environ.get('DJANGO_Q_REDIS_PASSWORD', ''),
    },

    # Optional: label for the ORM broker (alternative to Redis)
    # 'orm': 'default',  # Use Django ORM as broker instead of Redis
}

# ---------------------------------------------------------------------------
# Email (SMTP) Configuration
# ---------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.environ.get('REPORT_EMAIL_FROM', 'noreply@example.com')

# ---------------------------------------------------------------------------
# django-seed Email Automation Settings
# ---------------------------------------------------------------------------
# Path to the CSV file containing email recipients
EMAILS_CSV_PATH = os.environ.get('EMAILS_CSV_PATH', 'emails.csv')

# Base URL used to generate invitation links in emails
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')

# Reporting email addresses (do NOT hardcode - use .env)
REPORT_EMAIL_FROM = os.environ.get('REPORT_EMAIL_FROM', 'reports@example.com')
REPORT_EMAIL_TO = os.environ.get('REPORT_EMAIL_TO', 'admin@example.com')

# ---------------------------------------------------------------------------
# Template Configuration
# ---------------------------------------------------------------------------
# Ensure Django can find templates inside installed apps (APP_DIRS=True is
# sufficient when templates live in <app>/templates/).
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],          # Add project-level template dirs here if needed
        'APP_DIRS': True,    # Enables <app>/templates/ discovery
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
