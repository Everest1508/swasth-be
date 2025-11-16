from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, Prescription, PrescriptionMedicine
from .serializers import AppointmentSerializer, PrescriptionSerializer, PrescriptionMedicineSerializer
from doctors.models import DoctorSchedule


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for appointment management
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'consultation_type', 'doctor', 'patient']
    search_fields = ['symptoms']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Appointment.objects.none()
        
        # Handle special case: doctor=me in query params
        doctor_param = self.request.query_params.get('doctor', None)
        
        if user.role == 'patient':
            queryset = Appointment.objects.filter(patient__user=user)
        elif user.role == 'doctor':
            # For doctors, always filter by their own appointments
            # If doctor=me is provided, ignore it (already filtered)
            queryset = Appointment.objects.filter(doctor__user=user)
        elif user.role == 'admin':
            queryset = Appointment.objects.all()
            # Admin can filter by specific doctor if provided (but not 'me')
            if doctor_param and doctor_param != 'me':
                queryset = queryset.filter(doctor_id=doctor_param)
        
        return queryset
    
    def filter_queryset(self, queryset):
        """
        Override to handle doctor=me parameter before Django Filter processes it
        """
        # Remove doctor=me from query params before filtering
        if 'doctor' in self.request.query_params and self.request.query_params['doctor'] == 'me':
            # Create a mutable copy
            mutable_query_params = self.request.query_params.copy()
            mutable_query_params.pop('doctor')
            # Temporarily replace query_params
            original_params = self.request.query_params
            self.request._request.GET = mutable_query_params
            try:
                queryset = super().filter_queryset(queryset)
            finally:
                # Restore original
                self.request._request.GET = original_params
        else:
            queryset = super().filter_queryset(queryset)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def check_availability(self, request):
        """
        Check doctor availability for a given date and time
        """
        doctor_id = request.data.get('doctor_id')
        appointment_date = request.data.get('appointment_date')
        appointment_time = request.data.get('appointment_time')
        
        if not all([doctor_id, appointment_date, appointment_time]):
            return Response({'error': 'doctor_id, appointment_date, and appointment_time required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Check if doctor has schedule for that day
        appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M:%S")
        day_name = appointment_datetime.strftime('%A').lower()
        
        try:
            schedule = DoctorSchedule.objects.get(doctor_id=doctor_id, day=day_name, is_available=True)
            # Check if time is within schedule
            time_obj = datetime.strptime(appointment_time, "%H:%M:%S").time()
            if schedule.start_time <= time_obj <= schedule.end_time:
                # Check if slot is already booked
                existing = Appointment.objects.filter(
                    doctor_id=doctor_id,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    status__in=['pending', 'confirmed']
                )
                if existing.exists():
                    return Response({'available': False, 'reason': 'Slot already booked'})
                return Response({'available': True})
            return Response({'available': False, 'reason': 'Outside doctor schedule'})
        except DoctorSchedule.DoesNotExist:
            return Response({'available': False, 'reason': 'Doctor not available on this day'})
    
    @action(detail=True, methods=['post'])
    def upload_prescription(self, request, pk=None):
        """
        Upload prescription file for an appointment
        """
        appointment = self.get_object()
        prescription_file = request.FILES.get('prescription_file')
        
        if not prescription_file:
            return Response({'error': 'prescription_file required'}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment.prescription_file = prescription_file
        appointment.save()
        
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Mark appointment as completed and add consultation summary
        """
        appointment = self.get_object()
        consultation_summary = request.data.get('consultation_summary')
        
        appointment.status = 'completed'
        if consultation_summary:
            appointment.consultation_summary = consultation_summary
        appointment.save()
        
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for prescriptions
    """
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Prescription.objects.filter(appointment__patient__user=user)
        elif user.role == 'doctor':
            return Prescription.objects.filter(appointment__doctor__user=user)
        return Prescription.objects.all()
