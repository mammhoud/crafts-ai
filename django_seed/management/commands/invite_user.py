"""
Management command: invite_user

Queues an invitation email for a specified user.
Usage:
    python manage.py invite_user --email user@example.com --role instructor
    python manage.py invite_user --email user@example.com --role instructor --force
"""

import logging

from django.core.management.base import BaseCommand, CommandError

from django_seed.services import InvitationService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Queue an invitation email for a specified user"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            required=True,
            help="Email address of the user to invite",
        )
        parser.add_argument(
            "--role",
            required=True,
            help="Role to assign to the user (e.g. instructor, manager, supervisor, content_manager)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help="Skip duplicate-prevention check and send even if recently invited",
        )

    def handle(self, *args, **options):
        email = options["email"].strip()
        role = options["role"].strip()
        force = options["force"]

        self.stdout.write(f"Inviting user: {email} (role={role}, force={force})")
        logger.info("invite_user_command_started", extra={"email": email, "role": role, "force": force})

        try:
            service = InvitationService()
            log = service.invite_user(email=email, role=role, force=force)

            msg = f"Invitation queued for {email} (EmailLog id={log.id}, status={log.status})"
            self.stdout.write(self.style.SUCCESS(msg))
            logger.info(
                "invite_user_command_success",
                extra={"email": email, "role": role, "log_id": log.id, "status": log.status},
            )

        except ValueError as exc:
            # Expected business-logic errors (already registered, recently invited, etc.)
            error_msg = str(exc)
            self.stderr.write(self.style.ERROR(f"Error: {error_msg}"))
            logger.warning(
                "invite_user_command_rejected",
                extra={"email": email, "role": role, "reason": error_msg},
            )
            raise CommandError(error_msg) from exc

        except Exception as exc:
            error_msg = str(exc)
            self.stderr.write(self.style.ERROR(f"Unexpected error: {error_msg}"))
            logger.error(
                "invite_user_command_failed",
                extra={"email": email, "role": role, "error": error_msg},
                exc_info=True,
            )
            raise CommandError(f"Failed to invite user: {error_msg}") from exc
