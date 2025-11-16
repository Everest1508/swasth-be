from django.db import models
from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    """
    Appointment booking model
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    CONSULTATION_TYPE_CHOICES = [
        ('video', 'Video Consultation'),
        ('audio', 'Audio Consultation'),
        ('chat', 'Chat Consultation'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPE_CHOICES, default='video')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    symptoms = models.TextField(null=True, blank=True)
    consultation_token = models.CharField(max_length=200, null=True, blank=True)  # For video session
    consultation_summary = models.TextField(null=True, blank=True)
    prescription_file = models.FileField(upload_to='prescriptions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_date', '-appointment_time']
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['doctor', 'status']),
            models.Index(fields=['appointment_date', 'appointment_time']),
        ]
    
    def __str__(self):
        return f"{self.patient.user.get_full_name()} - Dr. {self.doctor.user.get_full_name()} ({self.appointment_date})"


class Prescription(models.Model):
    """
    Prescription model linked to appointments
    """
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    notes = models.TextField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prescriptions'
    
    def __str__(self):
        return f"Prescription for {self.appointment}"


class PrescriptionMedicine(models.Model):
    """
    Medicines prescribed in a prescription
    """
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    medicine = models.ForeignKey('medicines.Medicine', on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)  # e.g., "2 times a day"
    duration = models.CharField(max_length=100)  # e.g., "5 days"
    quantity = models.IntegerField()
    instructions = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'prescription_medicines'
    
    def __str__(self):
        return f"{self.medicine.name} - {self.dosage}"
