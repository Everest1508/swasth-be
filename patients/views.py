from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, HealthRecord
from .serializers import PatientSerializer, HealthRecordSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for patient management
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Patient.objects.filter(user=user)
        elif user.role in ['doctor', 'admin']:
            return Patient.objects.all()
        return Patient.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def health_records(self, request, pk=None):
        patient = self.get_object()
        records = HealthRecord.objects.filter(patient=patient)
        serializer = HealthRecordSerializer(records, many=True)
        return Response(serializer.data)


class HealthRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for health records
    """
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return HealthRecord.objects.filter(patient__user=user)
        elif user.role == 'doctor':
            return HealthRecord.objects.filter(doctor__user=user)
        elif user.role == 'admin':
            return HealthRecord.objects.all()
        return HealthRecord.objects.none()
