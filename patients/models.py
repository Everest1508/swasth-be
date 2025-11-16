from django.db import models
from accounts.models import User


class Patient(models.Model):
    """
    Patient profile model
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100, default='Patiala')
    state = models.CharField(max_length=100, default='Punjab')
    pincode = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patients'
        indexes = [
            models.Index(fields=['village']),
            models.Index(fields=['district']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.village}"


class HealthRecord(models.Model):
    """
    Digital health records for patients
    """
    RECORD_TYPE_CHOICES = [
        ('prescription', 'Prescription'),
        ('lab_report', 'Lab Report'),
        ('diagnosis', 'Diagnosis'),
        ('vaccination', 'Vaccination'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='health_records/', null=True, blank=True)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'health_records'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['patient', 'record_type']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.title}"
