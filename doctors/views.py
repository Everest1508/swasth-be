from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Doctor, DoctorSchedule
from .serializers import DoctorSerializer, DoctorScheduleSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for doctor management
    """
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Doctor.objects.filter(user=user)
        elif user.role == 'admin':
            return Doctor.objects.all()
        return Doctor.objects.filter(is_available=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get', 'post'])
    def schedule(self, request, pk=None):
        doctor = self.get_object()
        if request.method == 'POST':
            serializer = DoctorScheduleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(doctor=doctor)
            return Response(serializer.data)
        schedules = DoctorSchedule.objects.filter(doctor=doctor)
        serializer = DoctorScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for doctor schedules
    """
    serializer_class = DoctorScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            return DoctorSchedule.objects.filter(doctor_id=doctor_id)
        return DoctorSchedule.objects.all()
