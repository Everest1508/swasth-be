from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, PharmacyInventoryViewSet

router = DefaultRouter()
router.register(r'master', MedicineViewSet, basename='medicine')
router.register(r'inventory', PharmacyInventoryViewSet, basename='pharmacy-inventory')

urlpatterns = [
    path('', include(router.urls)),
]

