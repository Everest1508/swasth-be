from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register(r'bookings', AppointmentViewSet, basename='appointment')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    path('', include(router.urls)),
]

