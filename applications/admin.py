from django.contrib import admin
from .models import DoctorApplication, PharmacyApplication


@admin.register(DoctorApplication)
class DoctorApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'specialization', 'status', 'created_at')
    list_filter = ('status', 'specialization', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'license_number')
    readonly_fields = ('created_at', 'updated_at', 'reviewed_at')


@admin.register(PharmacyApplication)
class PharmacyApplicationAdmin(admin.ModelAdmin):
    list_display = ('pharmacy_name', 'owner_name', 'email', 'village', 'status', 'created_at')
    list_filter = ('status', 'district', 'created_at')
    search_fields = ('pharmacy_name', 'owner_name', 'email', 'license_number')
    readonly_fields = ('created_at', 'updated_at', 'reviewed_at')

