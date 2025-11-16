from django.contrib import admin
from .models import Appointment, Prescription, PrescriptionMedicine


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'consultation_type', 'created_at')
    list_filter = ('status', 'consultation_type', 'appointment_date')
    search_fields = ('patient__user__username', 'doctor__user__username', 'symptoms')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'follow_up_date', 'created_at')
    search_fields = ('appointment__patient__user__username',)


@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'medicine', 'dosage', 'frequency', 'quantity')
    search_fields = ('medicine__name',)
