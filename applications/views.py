from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction
import secrets
import string
from .models import DoctorApplication, PharmacyApplication
from .serializers import (
    DoctorApplicationSerializer,
    PharmacyApplicationSerializer,
    ApplicationApprovalSerializer
)
from email_service.service import EmailService
from doctors.models import Doctor
from pharmacies.models import Pharmacy

User = get_user_model()


class DoctorApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for doctor applications
    """
    serializer_class = DoctorApplicationSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to apply
    
    def get_queryset(self):
        user = self.request.user
        queryset = DoctorApplication.objects.none()
        
        if user.is_authenticated:
            if user.role == 'admin':
                queryset = DoctorApplication.objects.all()
            elif user.role == 'doctor':
                queryset = DoctorApplication.objects.filter(user=user)
        
        # Filter by status if provided
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'approve', 'reject']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Approve doctor application and create user account
        """
        application = self.get_object()
        
        if application.status != 'pending':
            return Response(
                {'error': 'Application has already been processed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ApplicationApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        approval_status = serializer.validated_data['status']
        
        if approval_status == 'approved':
            with transaction.atomic():
                # Generate temporary password
                password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                
                # Create user account
                username = application.email.split('@')[0] + '_' + str(application.id)
                user = User.objects.create_user(
                    username=username,
                    email=application.email,
                    password=password,
                    phone=application.phone,
                    first_name=application.first_name,
                    last_name=application.last_name,
                    role='doctor',
                    is_verified=True
                )
                
                # Create doctor profile
                doctor = Doctor.objects.create(
                    user=user,
                    specialization=application.specialization,
                    qualification=application.qualification,
                    license_number=application.license_number,
                    experience_years=application.experience_years,
                    consultation_fee=application.consultation_fee,
                    bio=application.bio,
                    is_available=True
                )
                
                # Update application
                application.status = 'approved'
                application.user = user
                application.reviewed_by = request.user
                application.reviewed_at = timezone.now()
                application.save()
                
                # Send approval email
                EmailService.send_approval_email(
                    email=application.email,
                    name=f"{application.first_name} {application.last_name}",
                    user_type='doctor',
                    login_credentials={
                        'email': application.email,
                        'password': password
                    }
                )
                
                return Response({
                    'message': 'Application approved and user account created',
                    'user_id': user.id,
                    'doctor_id': doctor.id
                })
        else:
            # Reject application
            application.status = 'rejected'
            application.rejection_reason = serializer.validated_data.get('rejection_reason', '')
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
            
            # Send rejection email
            EmailService.send_rejection_email(
                email=application.email,
                name=f"{application.first_name} {application.last_name}",
                user_type='doctor',
                reason=application.rejection_reason
            )
            
            return Response({'message': 'Application rejected'})


class PharmacyApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for pharmacy applications
    """
    serializer_class = PharmacyApplicationSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to apply
    
    def get_queryset(self):
        user = self.request.user
        queryset = PharmacyApplication.objects.none()
        
        if user.is_authenticated:
            if user.role == 'admin':
                queryset = PharmacyApplication.objects.all()
            elif user.role == 'pharmacy':
                queryset = PharmacyApplication.objects.filter(user=user)
        
        # Filter by status if provided
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'approve', 'reject']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Approve pharmacy application and create user account
        """
        application = self.get_object()
        
        if application.status != 'pending':
            return Response(
                {'error': 'Application has already been processed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ApplicationApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        approval_status = serializer.validated_data['status']
        
        if approval_status == 'approved':
            with transaction.atomic():
                # Generate temporary password
                password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                
                # Create user account
                username = application.email.split('@')[0] + '_' + str(application.id)
                user = User.objects.create_user(
                    username=username,
                    email=application.email,
                    password=password,
                    phone=application.phone,
                    first_name=application.owner_name,
                    role='pharmacy',
                    is_verified=True
                )
                
                # Create pharmacy profile
                pharmacy = Pharmacy.objects.create(
                    user=user,
                    name=application.pharmacy_name,
                    address=application.address,
                    village=application.village,
                    district=application.district,
                    state=application.state,
                    pincode=application.pincode,
                    latitude=application.latitude,
                    longitude=application.longitude,
                    license_number=application.license_number,
                    is_active=True
                )
                
                # Update application
                application.status = 'approved'
                application.user = user
                application.reviewed_by = request.user
                application.reviewed_at = timezone.now()
                application.save()
                
                # Send approval email
                EmailService.send_approval_email(
                    email=application.email,
                    name=application.owner_name,
                    user_type='pharmacy',
                    login_credentials={
                        'email': application.email,
                        'password': password
                    }
                )
                
                return Response({
                    'message': 'Application approved and user account created',
                    'user_id': user.id,
                    'pharmacy_id': pharmacy.id
                })
        else:
            # Reject application
            application.status = 'rejected'
            application.rejection_reason = serializer.validated_data.get('rejection_reason', '')
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
            
            # Send rejection email
            EmailService.send_rejection_email(
                email=application.email,
                name=application.owner_name,
                user_type='pharmacy',
                reason=application.rejection_reason
            )
            
            return Response({'message': 'Application rejected'})

