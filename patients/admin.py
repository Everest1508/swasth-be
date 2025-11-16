from django.contrib import admin
from .models import Patient, HealthRecord


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'village', 'district', 'created_at')
    list_filter = ('gender', 'district', 'state')
    search_fields = ('user__username', 'user__email', 'user__phone', 'village', 'district')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_type', 'title', 'doctor', 'date', 'created_at')
    list_filter = ('record_type', 'date')
    search_fields = ('patient__user__username', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')
