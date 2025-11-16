from django.contrib import admin
from .models import SymptomCheck, SymptomCache


@admin.register(SymptomCheck)
class SymptomCheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'symptoms')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'symptoms')
    readonly_fields = ('created_at',)


@admin.register(SymptomCache)
class SymptomCacheAdmin(admin.ModelAdmin):
    list_display = ('symptom_hash', 'hit_count', 'last_accessed', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'last_accessed')
