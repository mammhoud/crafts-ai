"""
Email automation services for django-seed.

This package contains services for CSV parsing, email queue management,
email sending, invitation management, and report generation.
"""

from .csv_parser import CSVParser, EmailRecord
from .email_service import EmailService
from .invitation_service import InvitationService
from .queue_manager import EmailQueueManager
from .report_generator import ReportGenerator

__all__ = [
    'CSVParser',
    'EmailRecord',
    'EmailService',
    'EmailQueueManager',
    'InvitationService',
    'ReportGenerator',
]
