from django.db import models
from accounts.models import User


class DoctorApplication(models.Model):
    """
    Doctor application for joining the platform
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    
    # Professional Information
    specialization = models.CharField(max_length=50)
    qualification = models.CharField(max_length=200)
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bio = models.TextField(null=True, blank=True)
    
    # Documents
    license_document = models.FileField(upload_to='doctor_applications/licenses/', null=True, blank=True)
    qualification_document = models.FileField(upload_to='doctor_applications/qualifications/', null=True, blank=True)
    
    # Application Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(null=True, blank=True)
    
    # Admin who processed
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_doctor_applications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Created user (after approval)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_application')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctor_applications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.status}"


class PharmacyApplication(models.Model):
    """
    Pharmacy application for joining the platform
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Personal Information
    owner_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    
    # Pharmacy Information
    pharmacy_name = models.CharField(max_length=200)
    address = models.TextField()
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100, default='Patiala')
    state = models.CharField(max_length=100, default='Punjab')
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    
    # Documents
    license_document = models.FileField(upload_to='pharmacy_applications/licenses/', null=True, blank=True)
    
    # Application Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(null=True, blank=True)
    
    # Admin who processed
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_pharmacy_applications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Created user (after approval)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pharmacy_application')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pharmacy_applications'
        ordering = ['-created_at']
        verbose_name_plural = 'Pharmacy Applications'
    
    def __str__(self):
        return f"{self.pharmacy_name} - {self.status}"

