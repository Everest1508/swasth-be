from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    OTPLoginSerializer,
    OTPRequestSerializer
)
import random
import requests
import logging
from datetime import datetime, timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class OTPRequestView(generics.CreateAPIView):
    """
    Request OTP for phone-based login
    """
    permission_classes = [AllowAny]
    serializer_class = OTPRequestSerializer
    
    def send_otp_via_sms(self, mobile_number, otp):
        """
        Send OTP via 2Factor.in SMS API
        """
        try:
            api_key = settings.FACTOR2_API_KEY
            api_url = f'{settings.FACTOR2_API_URL}/{api_key}/SMS/{mobile_number}/{otp}'
            
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 2Factor.in returns Status as "Success" on success
            if data.get('Status') == 'Success':
                logger.info(f'OTP sent successfully to {mobile_number}')
                return True, None
            else:
                error_msg = data.get('Details', 'Failed to send OTP')
                logger.error(f'Failed to send OTP: {error_msg}')
                return False, error_msg
                
        except requests.exceptions.RequestException as e:
            logger.error(f'Error sending OTP via SMS: {str(e)}')
            return False, 'SMS service temporarily unavailable. Please try again later.'
        except Exception as e:
            logger.error(f'Unexpected error sending OTP: {str(e)}')
            return False, 'An error occurred while sending OTP.'
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        
        # Clean phone number (remove spaces, dashes, etc.)
        mobile_number = phone.replace(' ', '').replace('-', '').replace('+', '')
        
        # Ensure phone number starts with country code (91 for India)
        if not mobile_number.startswith('91'):
            # If it's a 10-digit number, add 91 prefix
            if len(mobile_number) == 10:
                mobile_number = '91' + mobile_number
            elif mobile_number.startswith('0'):
                mobile_number = '91' + mobile_number[1:]
        
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        # Get or create user
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={'username': phone, 'is_verified': False}
        )
        
        # Store OTP
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()
        
        # Send OTP via SMS
        success, error_message = self.send_otp_via_sms(mobile_number, otp)
        
        if success:
            return Response({
                'message': 'OTP sent successfully to your mobile number',
            }, status=status.HTTP_200_OK)
        else:
            # Even if SMS fails, we still return success but log the error
            # This allows OTP verification to work in case SMS delivery is delayed
            # In production, you might want to handle this differently
            logger.warning(f'OTP generated but SMS sending failed for {phone}: {error_message}')
            return Response({
                'message': 'OTP generated. SMS may be delayed.',
                'error': error_message if settings.DEBUG else None
            }, status=status.HTTP_200_OK)


class OTPLoginView(generics.CreateAPIView):
    """
    Login using OTP
    """
    permission_classes = [AllowAny]
    serializer_class = OTPLoginSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']
        
        try:
            user = User.objects.get(phone=phone)
            
            # Check if OTP is valid and not expired (5 minutes)
            if user.otp != otp:
                return Response(
                    {'error': 'Invalid OTP'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if user.otp_created_at:
                time_diff = timezone.now() - user.otp_created_at
                if time_diff > timedelta(minutes=5):
                    return Response(
                        {'error': 'OTP expired'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Clear OTP
            user.otp = None
            user.otp_created_at = None
            user.is_verified = True
            user.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
