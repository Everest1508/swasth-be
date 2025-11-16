from django.db import models


class SMTPConfiguration(models.Model):
    """
    SMTP Configuration for sending emails
    """
    name = models.CharField(max_length=100, unique=True, help_text="Configuration name")
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Should be encrypted in production
    from_email = models.EmailField()
    from_name = models.CharField(max_length=100, default='Nabha Health Connect')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'smtp_configurations'
        verbose_name = 'SMTP Configuration'
        verbose_name_plural = 'SMTP Configurations'
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"

