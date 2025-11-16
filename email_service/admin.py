from django.contrib import admin
from .models import SMTPConfiguration


@admin.register(SMTPConfiguration)
class SMTPConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'port', 'from_email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'host', 'from_email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'is_active')
        }),
        ('SMTP Server', {
            'fields': ('host', 'port', 'use_tls', 'use_ssl')
        }),
        ('Authentication', {
            'fields': ('username', 'password')
        }),
        ('Email Settings', {
            'fields': ('from_email', 'from_name')
        }),
    )

