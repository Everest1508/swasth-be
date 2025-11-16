from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Medicine, PharmacyInventory
from .serializers import MedicineSerializer, PharmacyInventorySerializer


class MedicineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for medicine master data
    """
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['dosage_form', 'manufacturer']
    search_fields = ['name', 'generic_name', 'brand']
    
    def get_queryset(self):
        return Medicine.objects.all()


class PharmacyInventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for pharmacy inventory
    """
    serializer_class = PharmacyInventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['pharmacy', 'medicine', 'is_low_stock', 'is_out_of_stock']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'pharmacy':
            return PharmacyInventory.objects.filter(pharmacy__user=user)
        return PharmacyInventory.objects.all()
    
    @action(detail=False, methods=['get'])
    def availability(self, request):
        """
        Check medicine availability by area
        """
        medicine_id = request.query_params.get('medicine_id')
        village = request.query_params.get('village')
        district = request.query_params.get('district')
        
        queryset = PharmacyInventory.objects.filter(
            medicine_id=medicine_id,
            stock_quantity__gt=0
        )
        
        if village:
            queryset = queryset.filter(pharmacy__village=village)
        if district:
            queryset = queryset.filter(pharmacy__district=district)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Get low stock alerts
        """
        user = self.request.user
        if user.role == 'pharmacy':
            queryset = PharmacyInventory.objects.filter(
                pharmacy__user=user,
                stock_quantity__lte=models.F('low_stock_threshold')
            )
        else:
            queryset = PharmacyInventory.objects.filter(
                stock_quantity__lte=models.F('low_stock_threshold')
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
