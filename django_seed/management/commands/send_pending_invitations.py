"""
Management command: send_pending_invitations

Processes all pending (QUEUED) invitation EmailLog entries and attempts
to send each one immediately via EmailService._send_now().

Usage:
    python manage.py send_pending_invitations
    python manage.py send_pending_invitations --limit 50
"""

import logging

from django.core.management.base import BaseCommand

from django_seed.models import EmailLog
from django_seed.services import EmailService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Process all pending (QUEUED) invitations and attempt to send them"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            metavar="N",
            help="Process at most N pending invitations (default: all)",
        )

    def handle(self, *args, **options):
        limit = options["limit"]

        self.stdout.write("Processing pending invitations…")
        logger.info("send_pending_invitations_started", extra={"limit": limit})

        try:
            qs = EmailLog.objects.filter(status=EmailLog.Status.QUEUED).order_by("timestamp")
            if limit is not None:
                qs = qs[:limit]

            pending = list(qs)
            total = len(pending)
            self.stdout.write(f"Found {total} pending invitation(s).")
            logger.info("send_pending_invitations_count", extra={"total": total})

            sent = 0
            failed = 0

            email_service = EmailService()
            for log in pending:
                try:
                    self.stdout.write(f"  Sending to {log.recipient} (id={log.id})…")
                    email_service._send_now(
                        recipient=log.recipient,
                        subject=log.subject,
                        template_name=log.template_used or "emails/invitation.html",
                        context={},
                        log=log,
                    )
                    sent += 1
                    self.stdout.write(self.style.SUCCESS(f"  ✓ Sent to {log.recipient}"))
                    logger.info(
                        "send_pending_invitation_sent",
                        extra={"log_id": log.id, "recipient": log.recipient},
                    )

                except Exception as exc:
                    failed += 1
                    error_msg = str(exc)
                    self.stderr.write(
                        self.style.ERROR(f"  ✗ Failed for {log.recipient}: {error_msg}")
                    )
                    logger.error(
                        "send_pending_invitation_failed",
                        extra={"log_id": log.id, "recipient": log.recipient, "error": error_msg},
                        exc_info=True,
                    )
                    # mark_failed already called inside _send_now; continue with next

            summary = f"Done. Sent: {sent}, Failed: {failed}, Total: {total}"
            self.stdout.write(self.style.SUCCESS(summary))
            logger.info(
                "send_pending_invitations_complete",
                extra={"sent": sent, "failed": failed, "total": total},
            )

        except Exception as exc:
            error_msg = str(exc)
            self.stderr.write(self.style.ERROR(f"Unexpected error: {error_msg}"))
            logger.error(
                "send_pending_invitations_error",
                extra={"error": error_msg},
                exc_info=True,
            )
            # Re-raise so Django reports a non-zero exit code
            raise
