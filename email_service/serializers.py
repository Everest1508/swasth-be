from rest_framework import serializers
from .models import SMTPConfiguration


class SMTPConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPConfiguration
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False, 'allow_blank': True}
        }
    
    def update(self, instance, validated_data):
        # If password is not provided, don't update it
        if 'password' in validated_data and not validated_data['password']:
            validated_data.pop('password')
        return super().update(instance, validated_data)

