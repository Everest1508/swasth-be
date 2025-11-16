from django.db import models
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment


class DoctorAvailabilityMetric(models.Model):
    """
    Track doctor availability vs demand
    """
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability_metrics')
    date = models.DateField()
    total_slots = models.IntegerField(default=0)
    booked_slots = models.IntegerField(default=0)
    available_slots = models.IntegerField(default=0)
    no_show_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'doctor_availability_metrics'
        unique_together = ['doctor', 'date']
        indexes = [
            models.Index(fields=['doctor', 'date']),
        ]
    
    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.date}"


class HealthIssueMetric(models.Model):
    """
    Track most common health issues
    """
    issue_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, null=True, blank=True)
    patient_count = models.IntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'health_issue_metrics'
        indexes = [
            models.Index(fields=['issue_name', 'date']),
        ]
    
    def __str__(self):
        return f"{self.issue_name} - {self.patient_count} patients"


class PharmacyStockMetric(models.Model):
    """
    Track pharmacy stock trends
    """
    pharmacy = models.ForeignKey('pharmacies.Pharmacy', on_delete=models.CASCADE, related_name='stock_metrics')
    medicine = models.ForeignKey('medicines.Medicine', on_delete=models.CASCADE, related_name='stock_metrics')
    date = models.DateField()
    stock_quantity = models.IntegerField()
    low_stock_alerts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'pharmacy_stock_metrics'
        indexes = [
            models.Index(fields=['pharmacy', 'date']),
        ]
    
    def __str__(self):
        return f"{self.pharmacy.name} - {self.medicine.name} - {self.date}"


class TeleconsultationMetric(models.Model):
    """
    Track teleconsultation success metrics
    """
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='teleconsultation_metric')
    consultation_duration = models.IntegerField(null=True, blank=True)  # in minutes
    connection_quality = models.CharField(max_length=20, null=True, blank=True)  # good, fair, poor
    was_successful = models.BooleanField(default=True)
    issues_encountered = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teleconsultation_metrics'
    
    def __str__(self):
        return f"Teleconsultation - {self.appointment}"
