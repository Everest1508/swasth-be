from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorApplicationViewSet, PharmacyApplicationViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorApplicationViewSet, basename='doctor-application')
router.register(r'pharmacies', PharmacyApplicationViewSet, basename='pharmacy-application')

urlpatterns = [
    path('', include(router.urls)),
]

