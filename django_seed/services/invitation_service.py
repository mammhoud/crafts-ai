"""
Invitation Service for managing user invitations.

Manages user invitations based on registration status.
Integrates with django-seed for database seeding.
"""

import logging
from datetime import timedelta
from typing import List

from django.contrib.auth import get_user_model
from django.utils import timezone

from .csv_parser import CSVParser, EmailRecord
from .email_service import EmailService

User = get_user_model()
logger = logging.getLogger(__name__)


class InvitationService:
    """
    Manages user invitations based on registration status.
    Integrates with django-seed for database seeding.
    """

    DUPLICATE_PREVENTION_DAYS = 7

    def __init__(self, csv_path: str = 'emails.csv'):
        self.csv_path = csv_path
        self.email_service = EmailService()
        self.csv_parser = CSVParser(csv_path)

    def send_invitations_from_csv(self) -> List:
        """
        Read emails.csv and send invitations to unregistered users.
        Respects 7-day duplicate prevention rule.

        Returns:
            List of EmailLog instances for sent invitations
        """
        # Parse CSV
        records = self.csv_parser.parse()

        # Filter unregistered users
        unregistered = self._filter_unregistered(records)

        # Filter out recently invited
        to_invite = self._filter_recently_invited(unregistered)

        # Send invitations
        logs = []
        for record in to_invite:
            log = self._send_invitation(record)
            logs.append(log)

        logger.info(
            f"Invitations sent: {len(logs)} out of {len(records)} total records "
            f"({len(unregistered)} unregistered)"
        )

        return logs

    def invite_user(
        self,
        email: str,
        role: str,
        force: bool = False
    ):
        """
        Invite a single user.

        Args:
            email: User email address
            role: User role
            force: Skip duplicate prevention check

        Returns:
            EmailLog instance
        """
        # Check if user is registered
        if User.objects.filter(email=email).exists():
            logger.warning(f"User already registered: {email}")
            raise ValueError(f"User already registered: {email}")

        # Check duplicate prevention
        if not force and self._was_recently_invited(email):
            logger.warning(f"User recently invited: {email}")
            raise ValueError(
                f"User was invited within last {self.DUPLICATE_PREVENTION_DAYS} days"
            )

        # Send invitation
        record = EmailRecord(email=email, roles=[role])
        return self._send_invitation(record)

    def _filter_unregistered(self, records: List[EmailRecord]) -> List[EmailRecord]:
        """Filter out registered users."""
        registered_emails = set(
            User.objects.filter(
                email__in=[r.email for r in records]
            ).values_list('email', flat=True)
        )

        return [r for r in records if r.email not in registered_emails]

    def _filter_recently_invited(self, records: List[EmailRecord]) -> List[EmailRecord]:
        """Filter out users invited within last 7 days."""
        from ..models import EmailLog

        cutoff = timezone.now() - timedelta(days=self.DUPLICATE_PREVENTION_DAYS)

        recently_invited = set(
            EmailLog.objects.filter(
                recipient__in=[r.email for r in records],
                timestamp__gte=cutoff,
                status__in=[EmailLog.Status.SENT, EmailLog.Status.QUEUED]
            ).values_list('recipient', flat=True)
        )

        return [r for r in records if r.email not in recently_invited]

    def _was_recently_invited(self, email: str) -> bool:
        """Check if email was invited within last 7 days."""
        from ..models import EmailLog

        cutoff = timezone.now() - timedelta(days=self.DUPLICATE_PREVENTION_DAYS)

        return EmailLog.objects.filter(
            recipient=email,
            timestamp__gte=cutoff,
            status__in=[EmailLog.Status.SENT, EmailLog.Status.QUEUED]
        ).exists()

    def _send_invitation(self, record: EmailRecord):
        """Send invitation email for a record."""
        context = {
            'email': record.email,
            'role': record.primary_role,
            'roles': record.roles,
            'invitation_link': self._generate_invitation_link(record.email),
            'subject': 'You are invited to join our platform!'
        }

        return self.email_service.send_invitation(
            recipient=record.email,
            template_name='emails/invitation.html',
            context=context,
            queue=True
        )

    def _generate_invitation_link(self, email: str) -> str:
        """Generate invitation link for user."""
        try:
            from django.contrib.auth.tokens import default_token_generator
            from django.urls import reverse
            from django.utils.encoding import force_bytes
            from django.utils.http import urlsafe_base64_encode

            # Generate token
            token = default_token_generator.make_token(User())
            uid = urlsafe_base64_encode(force_bytes(email))

            # Build full URL
            try:
                path = reverse('invitation_accept', kwargs={'uidb64': uid, 'token': token})
            except:
                # Fallback if URL pattern doesn't exist
                path = f'/invitation/accept/{uid}/{token}/'

            return f"{self._get_site_url()}{path}"
        except Exception as e:
            logger.warning(f"Failed to generate invitation link: {e}")
            return f"{self._get_site_url()}/register/"

    def _get_site_url(self) -> str:
        """Get site URL from settings."""
        from django.conf import settings
        return getattr(settings, 'SITE_URL', 'http://localhost:8000')
