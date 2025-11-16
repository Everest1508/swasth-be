from django.db import models
from accounts.models import User


class SymptomCheck(models.Model):
    """
    AI Symptom Checker results
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symptom_checks', null=True, blank=True)
    symptoms = models.TextField()  # JSON or comma-separated symptoms
    probable_conditions = models.JSONField()  # Store AI model predictions
    confidence_scores = models.JSONField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'symptom_checks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"Symptom Check - {self.created_at}"


class SymptomCache(models.Model):
    """
    Cache frequently used symptom combinations for faster responses
    """
    symptom_hash = models.CharField(max_length=64, unique=True)  # Hash of symptoms
    symptoms = models.TextField()
    probable_conditions = models.JSONField()
    confidence_scores = models.JSONField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)
    hit_count = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'symptom_cache'
        indexes = [
            models.Index(fields=['symptom_hash']),
        ]
    
    def __str__(self):
        return f"Cached Symptom - {self.symptom_hash[:16]}"
