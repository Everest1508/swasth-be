from django.contrib import admin
from .models import Medicine, PharmacyInventory


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'dosage_form', 'strength', 'manufacturer', 'created_at')
    list_filter = ('dosage_form', 'manufacturer')
    search_fields = ('name', 'generic_name', 'brand', 'manufacturer')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PharmacyInventory)
class PharmacyInventoryAdmin(admin.ModelAdmin):
    list_display = ('pharmacy', 'medicine', 'stock_quantity', 'price', 'is_low_stock', 'last_updated')
    list_filter = ('pharmacy', 'stock_quantity')
    search_fields = ('pharmacy__name', 'medicine__name')
    readonly_fields = ('last_updated', 'created_at', 'is_low_stock', 'is_out_of_stock')
