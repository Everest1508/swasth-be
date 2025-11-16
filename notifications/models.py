from django.db import models
from accounts.models import User


class Notification(models.Model):
    """
    Notification model for users
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('appointment_reminder', 'Appointment Reminder'),
        ('prescription_ready', 'Prescription Ready'),
        ('medicine_stock', 'Medicine Stock Alert'),
        ('appointment_confirmed', 'Appointment Confirmed'),
        ('appointment_cancelled', 'Appointment Cancelled'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    sent_via_whatsapp = models.BooleanField(default=False)
    sent_via_push = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class NotificationTemplate(models.Model):
    """
    Templates for different notification types
    """
    notification_type = models.CharField(max_length=30, unique=True)
    title_template = models.CharField(max_length=200)
    message_template = models.TextField()
    sms_template = models.TextField(null=True, blank=True)
    whatsapp_template = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_templates'
    
    def __str__(self):
        return f"Template - {self.notification_type}"
