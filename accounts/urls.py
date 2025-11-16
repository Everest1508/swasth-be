from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import (
    UserRegistrationView,
    UserProfileView,
    OTPRequestView,
    OTPLoginView
)

app_name = 'accounts'

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User Management
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # OTP-based Authentication
    path('otp/request/', OTPRequestView.as_view(), name='otp_request'),
    path('otp/login/', OTPLoginView.as_view(), name='otp_login'),
]

