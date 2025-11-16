from rest_framework import serializers
from .models import Medicine, PharmacyInventory


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PharmacyInventorySerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_brand = serializers.CharField(source='medicine.brand', read_only=True)
    pharmacy_name = serializers.CharField(source='pharmacy.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_out_of_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = PharmacyInventory
        fields = '__all__'
        read_only_fields = ('last_updated', 'created_at')

