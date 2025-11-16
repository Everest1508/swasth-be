from rest_framework import serializers
from .models import SymptomCheck, SymptomCache


class SymptomCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomCheck
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class SymptomCheckRequestSerializer(serializers.Serializer):
    symptoms = serializers.CharField(required=True, help_text="Comma-separated symptoms or JSON string")

