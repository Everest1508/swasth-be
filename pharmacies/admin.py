from django.contrib import admin
from .models import Pharmacy


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'village', 'district', 'license_number', 'is_active', 'created_at')
    list_filter = ('district', 'is_active')
    search_fields = ('name', 'village', 'district', 'license_number', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
