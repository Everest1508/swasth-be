from rest_framework import serializers
from .models import DoctorAvailabilityMetric, HealthIssueMetric, PharmacyStockMetric, TeleconsultationMetric


class DoctorAvailabilityMetricSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    
    class Meta:
        model = DoctorAvailabilityMetric
        fields = '__all__'
        read_only_fields = ('created_at',)


class HealthIssueMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthIssueMetric
        fields = '__all__'
        read_only_fields = ('created_at',)


class PharmacyStockMetricSerializer(serializers.ModelSerializer):
    pharmacy_name = serializers.CharField(source='pharmacy.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    
    class Meta:
        model = PharmacyStockMetric
        fields = '__all__'
        read_only_fields = ('created_at',)


class TeleconsultationMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeleconsultationMetric
        fields = '__all__'
        read_only_fields = ('created_at',)

