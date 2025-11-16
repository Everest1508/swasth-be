from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, HealthRecordViewSet

router = DefaultRouter()
router.register(r'profiles', PatientViewSet, basename='patient')
router.register(r'health-records', HealthRecordViewSet, basename='health-record')

urlpatterns = [
    path('', include(router.urls)),
]

