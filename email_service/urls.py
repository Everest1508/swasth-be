from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SMTPConfigurationViewSet

router = DefaultRouter()
router.register(r'', SMTPConfigurationViewSet, basename='smtp-configuration')

urlpatterns = [
    path('', include(router.urls)),
]

