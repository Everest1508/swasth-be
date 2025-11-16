from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pharmacy
from .serializers import PharmacySerializer


class PharmacyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for pharmacy management
    """
    serializer_class = PharmacySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['village', 'district', 'is_active']
    search_fields = ['name', 'village', 'district']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'pharmacy':
            return Pharmacy.objects.filter(user=user)
        return Pharmacy.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def nearest(self, request):
        """
        Find nearest pharmacies based on coordinates
        """
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        
        if not lat or not lon:
            return Response({'error': 'latitude and longitude required'}, status=400)
        
        # TODO: Implement distance calculation
        pharmacies = Pharmacy.objects.filter(is_active=True)[:10]
        serializer = self.get_serializer(pharmacies, many=True)
        return Response(serializer.data)
