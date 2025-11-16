from django.db import models
from accounts.models import User


class Pharmacy(models.Model):
    """
    Pharmacy model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacy_profile')
    name = models.CharField(max_length=200)
    address = models.TextField()
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100, default='Patiala')
    state = models.CharField(max_length=100, default='Punjab')
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pharmacies'
        verbose_name_plural = 'Pharmacies'
        indexes = [
            models.Index(fields=['village']),
            models.Index(fields=['district']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.village}"
