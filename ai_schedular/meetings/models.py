from django.db import models


class Meeting(models.Model):
    """
    Model representing a scheduled meeting.
    """
    PLATFORM_CHOICES = [
        ('zoom', 'Zoom'),
        ('google', 'Google Meet'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    host_email = models.EmailField()
    participant_emails = models.TextField(
        help_text="Comma-separated list of participant email addresses."
    )
    scheduled_time = models.DateTimeField()
    meeting_link = models.URLField(blank=True, null=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        help_text="Current status of the meeting."
    )
    passcode = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    class Meta:
        ordering = ['-scheduled_time']