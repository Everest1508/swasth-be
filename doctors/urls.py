from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, DoctorScheduleViewSet

router = DefaultRouter()
router.register(r'profiles', DoctorViewSet, basename='doctor')
router.register(r'schedules', DoctorScheduleViewSet, basename='doctor-schedule')

urlpatterns = [
    path('', include(router.urls)),
]

