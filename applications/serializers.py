from rest_framework import serializers
from .models import DoctorApplication, PharmacyApplication


class DoctorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorApplication
        fields = '__all__'
        read_only_fields = ('status', 'reviewed_by', 'reviewed_at', 'user', 'created_at', 'updated_at')


class PharmacyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyApplication
        fields = '__all__'
        read_only_fields = ('status', 'reviewed_by', 'reviewed_at', 'user', 'created_at', 'updated_at')


class ApplicationApprovalSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['approved', 'rejected'])
    rejection_reason = serializers.CharField(required=False, allow_blank=True)

