from rest_framework import serializers
from .models import Patient, HealthRecord


class PatientSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class HealthRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = HealthRecord
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

