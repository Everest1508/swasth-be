from django.db import models
from pharmacies.models import Pharmacy


class Medicine(models.Model):
    """
    Medicine master data
    """
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, null=True, blank=True)
    generic_name = models.CharField(max_length=200, null=True, blank=True)
    dosage_form = models.CharField(max_length=50)  # e.g., "Tablet", "Syrup", "Injection"
    strength = models.CharField(max_length=50)  # e.g., "500mg", "10ml"
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medicines'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['generic_name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.strength})"


class PharmacyInventory(models.Model):
    """
    Medicine inventory for each pharmacy
    """
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='inventory')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='pharmacy_inventory')
    stock_quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    low_stock_threshold = models.IntegerField(default=10)  # Alert when stock goes below this
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'pharmacy_inventory'
        ordering = ['-last_updated']
        unique_together = ['pharmacy', 'medicine']
        indexes = [
            models.Index(fields=['pharmacy', 'stock_quantity']),
        ]
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.low_stock_threshold
    
    @property
    def is_out_of_stock(self):
        return self.stock_quantity == 0
    
    def __str__(self):
        return f"{self.pharmacy.name} - {self.medicine.name} (Stock: {self.stock_quantity})"
