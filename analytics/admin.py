from django.contrib import admin
from .models import DoctorAvailabilityMetric, HealthIssueMetric, PharmacyStockMetric, TeleconsultationMetric


@admin.register(DoctorAvailabilityMetric)
class DoctorAvailabilityMetricAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'total_slots', 'booked_slots', 'available_slots')
    list_filter = ('date',)
    search_fields = ('doctor__user__username',)


@admin.register(HealthIssueMetric)
class HealthIssueMetricAdmin(admin.ModelAdmin):
    list_display = ('issue_name', 'category', 'patient_count', 'date')
    list_filter = ('category', 'date')
    search_fields = ('issue_name',)


@admin.register(PharmacyStockMetric)
class PharmacyStockMetricAdmin(admin.ModelAdmin):
    list_display = ('pharmacy', 'medicine', 'stock_quantity', 'date')
    list_filter = ('date',)
    search_fields = ('pharmacy__name', 'medicine__name')


@admin.register(TeleconsultationMetric)
class TeleconsultationMetricAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'consultation_duration', 'connection_quality', 'was_successful', 'created_at')
    list_filter = ('was_successful', 'connection_quality', 'created_at')
    readonly_fields = ('created_at',)
