from django.contrib import admin
from .models import Doctor, DoctorSchedule


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'is_available', 'consultation_fee', 'created_at')
    list_filter = ('specialization', 'is_available')
    search_fields = ('user__username', 'user__email', 'license_number', 'specialization')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'start_time', 'end_time', 'is_available')
    list_filter = ('day', 'is_available')
    search_fields = ('doctor__user__username',)
