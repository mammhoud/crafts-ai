"""
Django models for email automation system.

This module contains models for tracking email logs, user roles, and user groups
for the email automation system.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class EmailLog(models.Model):
    """
    Audit trail for all email sending activities.
    Tracks delivery status, retries, and errors.
    """

    class Status(models.TextChoices):
        QUEUED = 'queued', 'Queued'
        SENDING = 'sending', 'Sending'
        SENT = 'sent', 'Sent'
        FAILED = 'failed', 'Failed'
        BOUNCED = 'bounced', 'Bounced'

    # Core fields
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    recipient = models.EmailField(db_index=True)
    subject = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.QUEUED,
        db_index=True
    )

    # Template and content
    template_used = models.CharField(max_length=255, blank=True)
    message_body = models.TextField(blank=True)

    # Error tracking
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    last_retry_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_logs'
    )
    group_name = models.CharField(max_length=100, blank=True)
    task_id = models.CharField(max_length=255, blank=True, db_index=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'email_log'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['status', 'timestamp']),
            models.Index(fields=['recipient', 'timestamp']),
            models.Index(fields=['task_id']),
        ]

    def __str__(self):
        return f"{self.recipient} - {self.subject} ({self.status})"

    def mark_sent(self):
        """Mark email as successfully sent."""
        self.status = self.Status.SENT
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at', 'updated_at'])

    def mark_failed(self, error_message: str):
        """Mark email as failed with error message."""
        self.status = self.Status.FAILED
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message', 'updated_at'])

    def increment_retry(self):
        """Increment retry count and update timestamp."""
        self.retry_count += 1
        self.last_retry_at = timezone.now()
        self.save(update_fields=['retry_count', 'last_retry_at', 'updated_at'])



class UserRole(models.Model):
    """
    Role assignment for users with hierarchical permissions.
    Supports multiple roles per user.
    """

    class Role(models.TextChoices):
        SUPERVISOR = 'supervisor', 'Supervisor'
        MANAGER = 'manager', 'Manager'
        INSTRUCTOR = 'instructor', 'Instructor'
        CONTENT_MANAGER = 'content_manager', 'Content Manager'

    # Role hierarchy (higher number = higher privilege)
    ROLE_HIERARCHY = {
        Role.SUPERVISOR: 4,
        Role.MANAGER: 3,
        Role.INSTRUCTOR: 2,
        Role.CONTENT_MANAGER: 1,
    }

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        db_index=True
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_roles'
    )

    class Meta:
        db_table = 'user_role'
        unique_together = [['user', 'role']]
        ordering = ['user', '-role']

    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"

    @classmethod
    def get_highest_role(cls, user):
        """Get the highest role for a user based on hierarchy."""
        user_roles = cls.objects.filter(user=user).values_list('role', flat=True)
        if not user_roles:
            return None

        highest = max(user_roles, key=lambda r: cls.ROLE_HIERARCHY.get(r, 0))
        return highest

    @classmethod
    def has_permission(cls, user, required_role):
        """Check if user has required role or higher."""
        user_highest = cls.get_highest_role(user)
        if not user_highest:
            return False

        user_level = cls.ROLE_HIERARCHY.get(user_highest, 0)
        required_level = cls.ROLE_HIERARCHY.get(required_role, 0)
        return user_level >= required_level



class UserGroup(models.Model):
    """
    User groups for targeted email distribution.
    Users can belong to multiple groups.
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='email_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_group'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_recipients(self):
        """Get all email addresses in this group."""
        return list(self.users.values_list('email', flat=True))
