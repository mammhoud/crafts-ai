"""
Unit tests for email automation models.
Tests EmailLog, UserRole, and UserGroup models.
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from django_seed.models import EmailLog, UserGroup, UserRole

User = get_user_model()


class EmailLogModelTestCase(TestCase):
    """Test cases for EmailLog model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_email_log(self):
        """Test creating an EmailLog instance."""
        log = EmailLog.objects.create(
            recipient='recipient@example.com',
            subject='Test Email',
            status=EmailLog.Status.QUEUED,
            template_used='emails/invitation.html'
        )

        self.assertEqual(log.recipient, 'recipient@example.com')
        self.assertEqual(log.subject, 'Test Email')
        self.assertEqual(log.status, EmailLog.Status.QUEUED)
        self.assertEqual(log.retry_count, 0)
        self.assertIsNotNone(log.timestamp)
        self.assertIsNotNone(log.created_at)

    def test_email_log_str(self):
        """Test EmailLog string representation."""
        log = EmailLog.objects.create(
            recipient='test@example.com',
            subject='Test Subject',
            status=EmailLog.Status.SENT
        )

        expected = "test@example.com - Test Subject (sent)"
        self.assertEqual(str(log), expected)

    def test_mark_sent(self):
        """Test marking email as sent."""
        log = EmailLog.objects.create(
            recipient='test@example.com',
            subject='Test',
            status=EmailLog.Status.SENDING
        )

        self.assertIsNone(log.sent_at)
        log.mark_sent()

        log.refresh_from_db()
        self.assertEqual(log.status, EmailLog.Status.SENT)
        self.assertIsNotNone(log.sent_at)

    def test_mark_failed(self):
        """Test marking email as failed."""
        log = EmailLog.objects.create(
            recipient='test@example.com',
            subject='Test',
            status=EmailLog.Status.SENDING
        )

        error_msg = "SMTP connection failed"
        log.mark_failed(error_msg)

        log.refresh_from_db()
        self.assertEqual(log.status, EmailLog.Status.FAILED)
        self.assertEqual(log.error_message, error_msg)

    def test_increment_retry(self):
        """Test incrementing retry count."""
        log = EmailLog.objects.create(
            recipient='test@example.com',
            subject='Test',
            status=EmailLog.Status.FAILED
        )

        self.assertEqual(log.retry_count, 0)
        self.assertIsNone(log.last_retry_at)

        log.increment_retry()
        log.refresh_from_db()

        self.assertEqual(log.retry_count, 1)
        self.assertIsNotNone(log.last_retry_at)

        # Test multiple retries
        log.increment_retry()
        log.refresh_from_db()
        self.assertEqual(log.retry_count, 2)

    def test_email_log_with_user(self):
        """Test EmailLog with associated user."""
        log = EmailLog.objects.create(
            recipient='test@example.com',
            subject='Test',
            user=self.user
        )

        self.assertEqual(log.user, self.user)
        self.assertIn(log, self.user.email_logs.all())

    def test_email_log_ordering(self):
        """Test EmailLog ordering by timestamp."""
        log1 = EmailLog.objects.create(
            recipient='test1@example.com',
            subject='First',
            timestamp=timezone.now() - timedelta(hours=2)
        )
        log2 = EmailLog.objects.create(
            recipient='test2@example.com',
            subject='Second',
            timestamp=timezone.now() - timedelta(hours=1)
        )
        log3 = EmailLog.objects.create(
            recipient='test3@example.com',
            subject='Third',
            timestamp=timezone.now()
        )

        logs = list(EmailLog.objects.all())
        self.assertEqual(logs[0], log3)  # Most recent first
        self.assertEqual(logs[1], log2)
        self.assertEqual(logs[2], log1)


class UserRoleModelTestCase(TestCase):
    """Test cases for UserRole model."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.supervisor = User.objects.create_user(
            username='supervisor',
            email='supervisor@example.com',
            password='pass123'
        )

    def test_create_user_role(self):
        """Test creating a UserRole instance."""
        role = UserRole.objects.create(
            user=self.user1,
            role=UserRole.Role.INSTRUCTOR,
            assigned_by=self.supervisor
        )

        self.assertEqual(role.user, self.user1)
        self.assertEqual(role.role, UserRole.Role.INSTRUCTOR)
        self.assertEqual(role.assigned_by, self.supervisor)
        self.assertIsNotNone(role.assigned_at)

    def test_user_role_str(self):
        """Test UserRole string representation."""
        role = UserRole.objects.create(
            user=self.user1,
            role=UserRole.Role.MANAGER
        )

        expected = f"{self.user1.email} - Manager"
        self.assertEqual(str(role), expected)

    def test_role_hierarchy(self):
        """Test role hierarchy values."""
        self.assertEqual(UserRole.ROLE_HIERARCHY[UserRole.Role.SUPERVISOR], 4)
        self.assertEqual(UserRole.ROLE_HIERARCHY[UserRole.Role.MANAGER], 3)
        self.assertEqual(UserRole.ROLE_HIERARCHY[UserRole.Role.INSTRUCTOR], 2)
        self.assertEqual(UserRole.ROLE_HIERARCHY[UserRole.Role.CONTENT_MANAGER], 1)

    def test_get_highest_role(self):
        """Test getting highest role for a user."""
        # User with no roles
        self.assertIsNone(UserRole.get_highest_role(self.user1))

        # User with single role
        UserRole.objects.create(user=self.user1, role=UserRole.Role.INSTRUCTOR)
        self.assertEqual(
            UserRole.get_highest_role(self.user1),
            UserRole.Role.INSTRUCTOR
        )

        # User with multiple roles
        UserRole.objects.create(user=self.user1, role=UserRole.Role.MANAGER)
        self.assertEqual(
            UserRole.get_highest_role(self.user1),
            UserRole.Role.MANAGER
        )

        # Add supervisor role (highest)
        UserRole.objects.create(user=self.user1, role=UserRole.Role.SUPERVISOR)
        self.assertEqual(
            UserRole.get_highest_role(self.user1),
            UserRole.Role.SUPERVISOR
        )

    def test_has_permission(self):
        """Test permission checking based on role hierarchy."""
        # User with no roles
        self.assertFalse(
            UserRole.has_permission(self.user1, UserRole.Role.INSTRUCTOR)
        )

        # User with instructor role
        UserRole.objects.create(user=self.user1, role=UserRole.Role.INSTRUCTOR)

        # Should have instructor permission
        self.assertTrue(
            UserRole.has_permission(self.user1, UserRole.Role.INSTRUCTOR)
        )

        # Should have content_manager permission (lower)
        self.assertTrue(
            UserRole.has_permission(self.user1, UserRole.Role.CONTENT_MANAGER)
        )

        # Should NOT have manager permission (higher)
        self.assertFalse(
            UserRole.has_permission(self.user1, UserRole.Role.MANAGER)
        )

        # Add manager role
        UserRole.objects.create(user=self.user1, role=UserRole.Role.MANAGER)

        # Now should have manager permission
        self.assertTrue(
            UserRole.has_permission(self.user1, UserRole.Role.MANAGER)
        )

        # Should still have instructor permission
        self.assertTrue(
            UserRole.has_permission(self.user1, UserRole.Role.INSTRUCTOR)
        )

    def test_unique_user_role_combination(self):
        """Test that user-role combination is unique."""
        UserRole.objects.create(
            user=self.user1,
            role=UserRole.Role.INSTRUCTOR
        )

        # Attempting to create duplicate should raise error
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            UserRole.objects.create(
                user=self.user1,
                role=UserRole.Role.INSTRUCTOR
            )

    def test_multiple_roles_per_user(self):
        """Test that a user can have multiple different roles."""
        UserRole.objects.create(user=self.user1, role=UserRole.Role.INSTRUCTOR)
        UserRole.objects.create(user=self.user1, role=UserRole.Role.MANAGER)

        roles = UserRole.objects.filter(user=self.user1)
        self.assertEqual(roles.count(), 2)


class UserGroupModelTestCase(TestCase):
    """Test cases for UserGroup model."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='pass123'
        )

    def test_create_user_group(self):
        """Test creating a UserGroup instance."""
        group = UserGroup.objects.create(
            name='Instructors',
            description='All instructors'
        )

        self.assertEqual(group.name, 'Instructors')
        self.assertEqual(group.description, 'All instructors')
        self.assertIsNotNone(group.created_at)
        self.assertIsNotNone(group.updated_at)

    def test_user_group_str(self):
        """Test UserGroup string representation."""
        group = UserGroup.objects.create(name='Test Group')
        self.assertEqual(str(group), 'Test Group')

    def test_add_users_to_group(self):
        """Test adding users to a group."""
        group = UserGroup.objects.create(name='Test Group')

        group.users.add(self.user1, self.user2)

        self.assertEqual(group.users.count(), 2)
        self.assertIn(self.user1, group.users.all())
        self.assertIn(self.user2, group.users.all())

    def test_get_recipients(self):
        """Test getting email addresses from a group."""
        group = UserGroup.objects.create(name='Test Group')
        group.users.add(self.user1, self.user2, self.user3)

        recipients = group.get_recipients()

        self.assertEqual(len(recipients), 3)
        self.assertIn('user1@example.com', recipients)
        self.assertIn('user2@example.com', recipients)
        self.assertIn('user3@example.com', recipients)

    def test_user_in_multiple_groups(self):
        """Test that a user can belong to multiple groups."""
        group1 = UserGroup.objects.create(name='Group 1')
        group2 = UserGroup.objects.create(name='Group 2')

        group1.users.add(self.user1)
        group2.users.add(self.user1)

        user_groups = self.user1.email_groups.all()
        self.assertEqual(user_groups.count(), 2)
        self.assertIn(group1, user_groups)
        self.assertIn(group2, user_groups)

    def test_unique_group_name(self):
        """Test that group names are unique."""
        UserGroup.objects.create(name='Unique Group')

        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            UserGroup.objects.create(name='Unique Group')

    def test_empty_group_recipients(self):
        """Test getting recipients from an empty group."""
        group = UserGroup.objects.create(name='Empty Group')
        recipients = group.get_recipients()

        self.assertEqual(len(recipients), 0)
        self.assertEqual(recipients, [])
