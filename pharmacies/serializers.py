from rest_framework import serializers
from .models import Pharmacy


class PharmacySerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    
    class Meta:
        model = Pharmacy
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

