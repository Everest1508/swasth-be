from rest_framework import serializers
from .models import Doctor, DoctorSchedule


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class DoctorSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    schedules = DoctorScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

