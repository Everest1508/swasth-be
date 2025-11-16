from rest_framework import serializers
from .models import Appointment, Prescription, PrescriptionMedicine


class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    
    class Meta:
        model = PrescriptionMedicine
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescriptionMedicineSerializer(many=True, read_only=True)
    appointment_id = serializers.IntegerField(source='appointment.id', read_only=True)
    
    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    prescription = PrescriptionSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

